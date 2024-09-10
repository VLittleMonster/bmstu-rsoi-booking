from enum import Enum
from schemas import dto


class ResponsesEnum(Enum):
    JWKsResponse = {
        "keys": [
            {
                "kty": "RSA",
                "use": "sig",
                "n": "zr3cfW6g1SC9Td4mlq6vQMDJNuyX5roqPyWUR9npVXX3qTuteeIUzoFl-SJcJdEob4Ee6gODSvSo3j_8nHtn6l8IYBQg_W3bQGP-XP_l-x4XUXSr7aPLcYmqdKo4oG8LW6CUoPl80DpWRRtKtH1Fgsx5kehi3QzjvtrycktJU0G5eIFMR9gVN1mqlSxle_0I-cJjdY8Ap7Y0fIOSPncG7Zycf6ItVjWjDQRheZAODSrMJDy1e0CEptUAdo-FrbuazLJby4M4Mb-RsazE7WyrtpEawRmAV-QbCfAYDLP_m-22J6CUc5r8iwRYA67IUZtg6XinMmVzdEZNyWJIiEY57w",
                "e": "AQAB",
                "kid": "uKfHXTZmkzhq4cpMlj_Ax",
                "x5t": "zpbmMLoyGkt_cVTLIyyrByLKLJw",
                "x5c": [
                    "t3u0FzMNLyRjAtH1X1yuowybtKrk41ezn1ThbtWOR1VYE7kl7nPnSWCVR-o1Kca2lVPZSM2wdUVss6hPvwHrHicsRDd_ZfiPU7PIyZTlbpVUkydfwtiW4Ymkp4-8Ip5POxkxI9TNQhedEl-NhKa3j6qHWvXQtnNXEqW0BZlZ956HazCI5_i3uIcVigEeWEyHIPjot4HrXkQtzbgpWGX3sN2K-ybq85LcNl1Ey_Iz8u3XoW-GClUZcV70PDg6e-JjLJQNCnhCuI0JcueqvWyQO7TFL39l_cofStazOYj-YTffJEh8FDXlQweDuGzgVvAlTOv3ctpr_Hgd9ivGUv_uPQ"
                ],
                "alg": "RS256"
            },
            {
                "kty": "RSA",
                "use": "sig",
                "n": "t3u0FzMNLyRjAtH1X1yuowybtKrk41ezn1ThbtWOR1VYE7kl7nPnSWCVR-o1Kca2lVPZSM2wdUVss6hPvwHrHicsRDd_ZfiPU7PIyZTlbpVUkydfwtiW4Ymkp4-8Ip5POxkxI9TNQhedEl-NhKa3j6qHWvXQtnNXEqW0BZlZ956HazCI5_i3uIcVigEeWEyHIPjot4HrXkQtzbgpWGX3sN2K-ybq85LcNl1Ey_Iz8u3XoW-GClUZcV70PDg6e-JjLJQNCnhCuI0JcueqvWyQO7TFL39l_cofStazOYj-YTffJEh8FDXlQweDuGzgVvAlTOv3ctpr_Hgd9ivGUv_uPQ",
                "e": "AQAB",
                "kid": "CRvTVKCJs453xaTDgNfrf",
                "x5t": "Ogu5lHQdpzlNVl7ejIDojJ5s-Dc",
                "x5c": [
                    "MIIDHTCCAgWgAwIBAgIJCPDmjV2EYh/6MA0GCSqGSIb3DQEBCwUAMCwxKjAoBgNVBAMTIWRldi02cG1waGtseGtzZ3IwNThqLnVzLmF1dGgwLmNvbTAeFw0yNDAxMTcxNDA2NDNaFw0zNzA5MjUxNDA2NDNaMCwxKjAoBgNVBAMTIWRldi02cG1waGtseGtzZ3IwNThqLnVzLmF1dGgwLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALd7tBczDS8kYwLR9V9crqMMm7Sq5ONXs59U4W7VjkdVWBO5Je5z50lglUfqNSnGtpVT2UjNsHVFbLOoT78B6x4nLEQ3f2X4j1OzyMmU5W6VVJMnX8LYluGJpKePvCKeTzsZMSPUzUIXnRJfjYSmt4+qh1r10LZzVxKltAWZWfeeh2swiOf4t7iHFYoBHlhMhyD46LeB615ELc24KVhl97Ddivsm6vOS3DZdRMvyM/Lt16FvhgpVGXFe9Dw4OnviYyyUDQp4QriNCXLnqr1skDu0xS9/Zf3KH0rWszmI/mE33yRIfBQ15UMHg7hs4FbwJUzr93Laa/x4HfYrxlL/7j0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUHq0KG0Ke7P8OGi5E97nufS9H7dYwDgYDVR0PAQH/BAQDAgKEMA0GCSqGSIb3DQEBCwUAA4IBAQCE3x6MNWrWIBfzcxyuEXmT8vGobb+423DCmQLgNPsRf6EPlOhLnzi+vJD7ZITVjBjIQfm9WaLcqWj/TtrtiB+D5/lnx5lc66y9aBq8yfZJEyrFqhQlr/1BPqa8yr4FrGzW2BUh20r4OOSrU48P9ifk4KceTw02lRzIE89st/cz5VY+DUNCmcR3FfY5U46ohj00m7ZK6RGzubWDTWIx0JddtI29xX96nPv5T5OZuVVyU0GJIdy9yU101H/nE1l9FsYE2cuppnYOEQ9CyfXzX4jZxG8t9gYj7ngxhEF32z1rRVC4go8A2thHeNCsZWgCR74UtD0gcme1c8A4pmMq5xFA"
                ],
                "alg": "RS256"
            },
        ]
    }



    TokenResponse = {
        "model": dto.TokenResponse
    }
