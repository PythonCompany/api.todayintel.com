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
package ru.sokomishalov.skraper.client.spring

import io.netty.handler.ssl.SslContextBuilder
import io.netty.handler.ssl.util.InsecureTrustManagerFactory
import org.springframework.http.client.reactive.ReactorClientHttpConnector
import reactor.netty.http.client.HttpClient
import ru.sokomishalov.skraper.client.SkraperClient
import ru.sokomishalov.skraper.client.SkraperClientTck
import ru.sokomishalov.skraper.client.spring.SpringReactiveSkraperClient.Companion.DEFAULT_CLIENT


/**
 * @author sokomishalov
 */
class SpringReactiveSkraperClientTest : SkraperClientTck() {
    override val client: SkraperClient = SpringReactiveSkraperClient(
        webClient = DEFAULT_CLIENT
            .mutate()
            .clientConnector(ReactorClientHttpConnector(
                HttpClient
                    .create()
                    .followRedirect(true)
                    .secure {
                        it.sslContext(
                            SslContextBuilder
                                .forClient()
                                .trustManager(InsecureTrustManagerFactory.INSTANCE)
                                .build()
                        )
                    }
            ))
            .build()
    )
}