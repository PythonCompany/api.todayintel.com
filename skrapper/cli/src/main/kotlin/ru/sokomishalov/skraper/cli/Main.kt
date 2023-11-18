/*
 * Copyright (c) 2019-present Mikhael Sokolov
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
@file:JvmName("Main")

package ru.sokomishalov.skraper.cli

import com.github.ajalt.mordant.TermColors
import com.xenomachina.argparser.ArgParser
import com.xenomachina.argparser.mainBody
import kotlinx.coroutines.asCoroutineDispatcher
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.flow.take
import kotlinx.coroutines.flow.toList
import kotlinx.coroutines.runBlocking
import me.tongfei.progressbar.ProgressBar
import ru.sokomishalov.skraper.Skrapers
import ru.sokomishalov.skraper.model.Post
import java.io.File
import java.time.LocalDateTime.now
import java.time.format.DateTimeFormatter.ofPattern
import java.util.*
import java.util.concurrent.Executors
import kotlin.system.exitProcess
import kotlin.text.Charsets.UTF_8

fun main(args: Array<String>) = mainBody(columns = 100) {
    val parsedArgs = ArgParser(args = args.ifEmpty { arrayOf("--help") }).parseInto(::Args)

    val posts = runBlocking {

            parsedArgs
                .skraper
                .getPosts("/${parsedArgs.path.removePrefix("/")}")
                .take(parsedArgs.limit)
                .toList()
    }

    when {
        parsedArgs.onlyMedia -> posts.persistMedia(parsedArgs)
        else -> posts.persistMeta(parsedArgs)
    }

}

private fun List<Post>.persistMedia(parsedArgs: Args) {
    val provider = parsedArgs.skraper.provider
    val requestedPath = parsedArgs.path
    val root = when {
        parsedArgs.output.isFile -> parsedArgs.output.parentFile.absolutePath
        else -> parsedArgs.output.absolutePath
    }
    val targetDir = File("${root}/${provider}/${requestedPath}").apply { mkdirs() }

    ProgressBar(with(t) { yellow("Fetching media") }, size.toLong()).use { pb ->
        runBlocking(context = Executors.newFixedThreadPool(parsedArgs.threads).asCoroutineDispatcher()) {
            flatMap { post ->
                post.media.mapIndexed { index, media ->
                    async {
                        runCatching {
                            Skrapers.download(
                                media = media,
                                destDir = targetDir,
                                filename = when (post.media.size) {
                                    1 -> post.id
                                    else -> "${post.id}_${index + 1}"
                                }
                            )
                        }.onSuccess { path ->
                            log { "${media.url} data has been written to ${cyan(path.absolutePath)}" }
                            pb.step()
                        }.onFailure { thr ->
                            log { "Cannot download ${media.url} , Reason: ${red(thr.toString())}" }
                        }
                    }
                }.awaitAll()
            }
        }
    }

    exitProcess(1)
}

private fun List<Post>.persistMeta(parsedArgs: Args) {
    val provider = parsedArgs.skraper.provider
    val requestedPath = parsedArgs.path

    val content = with(parsedArgs.outputType) { serialize() }

    val fileToWrite = when {
        parsedArgs.output.isFile -> parsedArgs.output
        else -> {
            val root = parsedArgs.output.absolutePath
            val now = now().format(ofPattern("ddMMyyyy'_'hhmmss"))
            val ext = parsedArgs.outputType.extension

            File("${root}/${provider}/${requestedPath}_${now}.${ext}")
        }
    }

    fileToWrite
        .apply { parentFile.mkdirs() }
        .writeText(text = content, charset = UTF_8)

    log { "${cyan(fileToWrite.path)}" }
}

private fun extractCurrentVersion(): String? {
    return runCatching {
        Properties()
            .apply { load(ClassLoader.getSystemResourceAsStream("git.properties")) }
            .getProperty("git.build.version")
    }.getOrNull()
}

private val toolName get() = with(t) {
    "${green("Scraper")}${extractCurrentVersion()?.let { " ${magenta(it)}" }.orEmpty()}"
}

private inline fun log(msg: TermColors.() -> String) = with(t) {
    println(msg())
}

@JvmField
val t = TermColors()
