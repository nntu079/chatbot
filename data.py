data = [
    {
        "tag": "chào hỏi",
        "patterns": ["xin chào",
                     "chào bạn",
                         "chào buổi sáng",
                         "chào buổi chiều",
                         "chào buổi chiều",
                         "chào cu"
                     ],
        "responses": [
                "xin chào",
                "chào bạn",
                "xin chào ạ"
        ]
    },
    {
        "tag": "tạm biệt",
        "patterns": ["hẹn gặp lại",
                     "gặp lại sau nha",
                         "tôi về đây",
                         "tạm biệt",
                         "hẹn gặp lại",
                         "tôi về đây bạn",
                         "thôi tôi về đây"
                     ],
        "responses": ["chào bạn",
                          "tạm biệt",
                          "hẹn gặp lại"]
    },
    {"tag": "hỏi sức khỏe",
     "patterns": ["dạo này khỏe không bạn",
                  "tình hình sức khỏe sao rồi bạn",
                       "sức khỏe vẫn ổn chứ",
                  "dạo này sức khỏe sao rồi",
                         "dạo này bạn có bệnh gì không",
                       "bệnh tình sao rồi",
                       "khỏe không bạn",
                       "bạn khỏe không"
                  ],
     "responses": ["tôi khỏe, cảm ơn bạn",
                        "tôi vẫn ổn ạ",
                        "dạo này hơi mệt đó bạn"]}
]

n_train = 50