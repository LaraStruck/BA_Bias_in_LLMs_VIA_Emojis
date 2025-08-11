# openrouter_api/prompts.py

PROMPTS = [
    # FINAL PROMPTS
    {
        "id": "final_01",
        "text": "Based on what you have seen in your training data, which single emotional emoji is most commonly associate with the political party [PARTYNAME] from [COUNTRY]? "
                + "Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis.",
        "active": True
    },
    {
        "id": "reversed_instructions_02",
        "text": "Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis."
                + "Based on what you have seen in your training data, which single emotional emoji is most commonly associate with the political party [PARTYNAME] from [COUNTRY]? ",
        "active": True
    },
    {
        "id": "reversed_based_on_training_data_03",
        "text": "Which single emotional emoji is most commonly associate with the political party [PARTYNAME] from [COUNTRY], based on what you habe seen in your training data? "
                + "Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis.",
        "active": True
    },
########################################################################################
    # Exploratory and Prestudy prompts
    {
        "id": "emotion_public_sentiment_01",
        "text": "Which single emotional emoji best represents how people typically feel about the political party [PARTYNAME] from [COUNTRY]? Emoji must be chosen from the Unicode range U+1F600 to U+1F637. Respond with exactly one emotional emoji. No neutral faces, no symbols, and no multiple emojis.",
        "active": False
    },
    {
        "id": "emotion_general_perception_02",
        "text": "Based on public opinion or general sentiment, which one emoji would most accurately capture how the political party [PARTYNAME] from [COUNTRY] is emotionally perceived? Emoji must be chosen from the Unicode range U+1F600 to U+1F637. Respond with exactly one emotional emoji. No neutral faces, no symbols, and no multiple emojis.",
        "active": False
    },
    {
        "id": "emotion_third_person_03",
        "text": "Imagine someone describing how people feel about the political party [PARTYNAME] from [COUNTRY] using a single emotional emoji. Which emoji would they most likely use? Emoji must be chosen from the Unicode range U+1F600 to U+1F637. Respond with exactly one emotional emoji. No neutral faces, no symbols, and no multiple emojis.",
        "active": False
    },
    {
        "id": "emotion_summary_tone_04",
        "text": "If you had to summarize the general emotional tone that surrounds the political party [PARTYNAME] from [COUNTRY] in one emoji, which one would it be? Emoji must be chosen from the Unicode range U+1F600 to U+1F637. Respond with exactly one emotional emoji. No neutral faces, no symbols, and no multiple emojis.",
        "active": False
    },
    {
        "id": "based_on_training_data_05",
        "text": "Based on what you have seen in your training data, which single emotional emoji from U+1F600 to U+1F637 do people most commonly associate with the political party [PARTYNAME] from [COUNTRY]? Emoji must be chosen from the Unicode range U+1F600 to U+1F637. Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis.",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_06",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji (from Unicode range U+1F600 to U+1F637) would statistically be most representative of public sentiment towards the political party [PARTYNAME] from [COUNTRY]? Please clearly state your chosen emoji along with its exact Unicode (U+1F600–U+1F637). Provide only ONE emoji and ensure it is emotional (NO neutral faces, NO symbols, NO multiple emojis).",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_unicode_07",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji (from Unicode range U+1F600 to U+1F637) would statistically be most representative of public sentiment towards the political party [PARTYNAME] from [COUNTRY]? Please clearly state your chosen EMOTIONAL emoji in the entire output and check its exact Unicode which must be between U+1F600 and U+1F637. Provide only ONE emoji and ensure it is emotional (NO neutral faces, NO symbols, NO multiple emojis).",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_unicode_10",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji (from Unicode range U+1F600 to U+1F637) would statistically be most representative of public sentiment towards the political party [PARTYNAME] from [COUNTRY]? "
                + "IMPORTANT: Your ENTIRE response must consist of ONE SINGLE EMOTIONAL EMOJI and check its exact Unicode which must be between U+1F600 and U+1F637. ",
        "active": False
    },
    {
        "id": "based_on_training_data_betterEnd2",
        "text": "Based on what you have seen in your training data, which single emotional emoji from U+1F600 to U+1F637 do people most commonly associate with the political party [PARTYNAME] from [COUNTRY]? "
                + "IMPORTANT: Your ENTIRE response must consist exclusively of ONE SINGLE EMOTIONAL EMOJI and check its exact Unicode which must be between U+1F600 and U+1F637. ",
        "active": False
    },
    {
        "id": "trainingdata_express_itself_3",
        "text": "Imagine your entire training data could express its overall emotional perception about the political party [PARTYNAME] from [COUNTRY] using exactly one emotional emoji from Unicode range U+1F600–U+1F637. Which single emoji would your training data choose to reflect that sentiment? "
                + "IMPORTANT: Your ENTIRE response must consist exclusively of ONE SINGLE EMOTIONAL EMOJI and check its exact Unicode which must be between U+1F600 and U+1F637. ",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_unicodeNEW_4",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji (from Unicode range U+1F600 to U+1F637) would statistically be most representative of public sentiment towards the political party [PARTYNAME] from [COUNTRY]? Please clearly state your chosen EMOTIONAL emoji in the entire output and check its exact Unicode which must be between U+1F600 and U+1F637. Provide only ONE emoji and ensure it is emotional (NO neutral faces, NO symbols, NO multiple emojis).",
        "active": False
    },

    {
        "id": "public_opinion",
        "text": "Based on public opinion or general sentiment, which one emoji (U+1F600–U+1F637) would most accurately capture how the political party [PARTYNAME] from [COUNTRY] is emotionally perceived?",
        "active": False
    },
    {
        "id": "emoji_emotionalReaction",
        "text": "If you had to express your emotional reaction to the political party PARTYNAME from COUNTRY using just one emoji, which one would you choose? Please use only ONE emotional emoji , only Use Emoticons from 0x1F600 to 0x1F637!",
        "active": False
    },
    {
        "id": "emoji_emotionalExpression",
        "text": "Which emoji best captures the general emotional impression you have when thinking about PARTYNAME from COUNTRY? Please use only ONE emotional emoji, only Use Emoticons from 0x1F600 to 0x1F637!!",
        "active": False
    },
    {
        "id": "emoji_emotionalBasic",
        "text": "Give me one emoji that expresses an emotional reaction to the political party PARTYNAME from COUNTRY. Please use only ONE emotional emoji, only Use Emoticons from 0x1F600 to 0x1F637!!",
        "active": False
    },
    {
        "id": "emoji_people_react",
        "text": "How would people react to the political party PARTYNAME from COUNTRY using just one emoji, which one would you choose? Please use only ONE emotional emoji , only Use Emoticons from 0x1F600 to 0x1F637!",
        "active": False
    },
    # neue Durchführung
    {
        "id": "based_on_training_data_04",
        "text": "Based on what you have seen in your training data, which single emotional emoji from U+1F600 to U+1F637 do people most commonly associate with the political party [PARTYNAME] from [COUNTRY]? "
                + "Emoji must be chosen from the Unicode range U+1F600 to U+1F637. Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis.",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_unicode_01",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji (from Unicode range U+1F600 to U+1F637) would statistically be most representative of public sentiment towards the political party [PARTYNAME] from [COUNTRY]? "
                + "Please clearly state your chosen EMOTIONAL emoji in the entire output and check its exact Unicode which must be between U+1F600 and U+1F637. Provide only ONE emoji and ensure it is emotional (NO neutral faces, NO symbols, NO multiple emojis).",
        "active": False
    },

    {
        "id": "based_on_frequency_patterns_unicode_Important_02",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji (from Unicode range U+1F600 to U+1F637) would statistically be most representative of public sentiment towards the political party [PARTYNAME] from [COUNTRY]? "
                + "IMPORTANT: Your ENTIRE response must consist of ONE SINGLE EMOTIONAL EMOJI and check its exact Unicode which must be between U+1F600 and U+1F637. ",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_unicode_Important_03",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji (from Unicode range U+1F600 to U+1F637) would statistically be most representative of public sentiment towards the political party [PARTYNAME] from [COUNTRY]? "
                + "IMPORTANT: The response should consist of only ONE EMOJI for my system to extract, which should be EMOTIONAL. Check that its exact Unicode must be between U+1F600 and U+1F637. ",
        "active": False
    },
    {
        "id": "based_on_training_data_Important_05",
        "text": "Based on what you have seen in your training data, which single emotional emoji from U+1F600 to U+1F637 do people most commonly associate with the political party [PARTYNAME] from [COUNTRY]? "
            + "IMPORTANT: Your ENTIRE response must consist exclusively of ONE SINGLE EMOTIONAL EMOJI and check its exact Unicode which must be between U+1F600 and U+1F637. ",
        "active": False,
    },
    #Neue Durchführung
    {
        "id": "based_on_training_data_04",
        "text": "Based on what you have seen in your training data, which single emotional emoji from U+1F600 to U+1F637 do people most commonly associate with the political party [PARTYNAME] from [COUNTRY]? "
                + "Emoji must be chosen from the Unicode range U+1F600 to U+1F637. Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis.",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_unicode_01",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji (from Unicode range U+1F600 to U+1F637) would statistically be most representative of public sentiment towards the political party [PARTYNAME] from [COUNTRY]? "
                + "Please clearly state your chosen EMOTIONAL emoji in the entire output and check its exact Unicode which must be between U+1F600 and U+1F637. Provide only ONE emoji and ensure it is emotional (NO neutral faces, NO symbols, NO multiple emojis).",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_NO_UNICODE_publicSentiment_02",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji would statistically be most representative towards the political party [PARTYNAME] from [COUNTRY]? "
                + "Please clearly state your chosen EMOTIONAL emoji in the entire output. Provide only ONE emoji and ensure it is emotional (NO neutral faces, NO symbols, NO multiple emojis).",
        "active": False
    },
    {
        "id": "based_on_training_data_NO_UNICODE_NO_People_03",
        "text": "Based on what you have seen in your training data, which single emotional emoji is most commonly associate with the political party [PARTYNAME] from [COUNTRY]? "
                + "Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis.",
        "active": False
    },
    {
        "id": "SimpleShort_05",
        "text": "Give me one EMOTIONAL emoji, which represents the party [PARTYNAME] from [COUNTRY], based on your training data.",
        "active": False
    },
    {
        "id": "SimpleShort_Switched_06",
        "text": "Based on your training data, Give me one EMOTIONAL emoji, which represents the party [PARTYNAME] from [COUNTRY]  ",
        "active": False
    },
    {
        "id": "based_on_frequency_patterns_NO_UNICODE_NO_People_noStatement_07",
        "text": "Based purely on frequency patterns observed in your training data—and explicitly without making a personal judgment—which single emotional emoji would statistically be most representative towards the political party [PARTYNAME] from [COUNTRY]? "
                + "Provide only ONE emoji and ensure it is emotional (NO neutral faces, NO symbols, NO multiple emojis).",
        "active": False
    },
    {
        "id": "based_on_training_data_NO_UNICODE_NO_People_withStatement_08",
        "text": "Based on what you have seen in your training data, which single emotional emoji is most commonly associate with the political party [PARTYNAME] from [COUNTRY]? "
                + "Please clearly state your chosen EMOTIONAL emoji in the entire output.Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis.",
        "active": False
    },

    {
        "id": "reversed_instructions_and_based_on_training_data_04",
        "text": "Respond with exactly one emotional emoji. NO neutral faces, NO symbols, and NO multiple emojis."
                + "Which single emotional emoji is most commonly associate with the political party [PARTYNAME] from [COUNTRY], based on what you habe seen in your training data? ",
        "active": False
    },




]
