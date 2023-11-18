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
package ru.sokomishalov.skraper.cli

import com.xenomachina.argparser.ArgParser
import com.xenomachina.argparser.default
import ru.sokomishalov.skraper.Skrapers
import ru.sokomishalov.skraper.cli.Serialization.LOG
import ru.sokomishalov.skraper.client.ktor.KtorSkraperClient
import java.io.File

class Args(parser: ArgParser) {

    init {
        Skrapers.client = KtorSkraperClient()
    }

    val skraper by parser.positional(
        name = "PROVIDER",
        help = "skraper provider, options: ${Skrapers.available().joinToString { it.provider }}"
    ) { Skrapers.available().find { this == it.provider }.let { requireNotNull(it) { "Unknown provider" } } }

    val path by parser.positional(
        name = "PATH",
        help = "path to user/community/channel/topic/trend"
    )

    val limit by parser.storing(
        "-n", "-l", "--limit",
        help = "posts limit (50 by default)"
    ) { toInt() }.default { 50 }

    val outputType by parser.storing(
        "-t", "--type",
        help = "output type, options: ${Serialization.values().joinToString().lowercase()}"
    ) { Serialization.valueOf(uppercase()) }.default { LOG }

    val output by parser.storing(
        "-o", "--output",
        help = "output path"
    ) { File(this) }.default { File("") }

    val onlyMedia by parser.flagging(
        "-m", "--media-only",
        help = "scrape media only"
    )

    val threads by parser.storing(
        "--parallel-downloads",
        help = "amount of parallel downloads for media items if enabled flag --media-only (4 by default)"
    ) { toInt() }.default { 4 }
}