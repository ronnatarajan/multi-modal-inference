# v3 vs v7 on dev questions 51-238

v3 = structured slots (`prompts/mainprompt_v3`). v7 = VIBE baseline + one voice sentence (`prompts/mainprompt_v7`).
Both prompts describe the voice: v7 asks for pitch, loudness, speed, pauses and emphasis; v3's tone slot asks for the same plus voice-quality words (shaky, breathy, tense, flat, strained).

On these 188 questions: v3 136, v7 137, baseline 140. They disagree on 39: v3 right only 19, v7 right only 20.

## Tag counts

**v3 right, v7 wrong (19)**  
cue: face 8, smile/laugh 6, hands/gesture 3, voice/speech 1, gaze 1  
emotions: joy 6, anger 6, intensity/emphasis 6, fear/anxiety 3, calm/relaxed 2, other 2, sadness 1  
negated questions: 5  
clips: 14

**v7 right, v3 wrong (20)**  
cue: face 9, hands/gesture 4, gaze 3, voice/speech 2, smile/laugh 1, posture/movement 1  
emotions: intensity/emphasis 6, engagement/attention 5, anger 5, joy 3, other 2, sadness 2, fear/anxiety 2, surprise 1  
negated questions: 7  
clips: 18

## v3 right, v7 wrong (19)

### `video_150_1` · cue: smile/laugh · emotions: joy, calm/relaxed · negated
**Fact:** There is a slight smile on the speaker's face.  
**Correct (A):** The slight smile does not indicate a relaxed and content expression.  
**Other (B):** The slight smile indicates a relaxed and content expression.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is low and the pace is slow. The voice is strained. | The speaker's voice is of a low pitch. The volume is consistent. The pace is moderate. There is a slight rise in pitch on the word "real." |
| Decider's reasoning | The speaker's overall body language—including narrowed eyes, a low and strained voice, and a slow, deliberate pace—suggests tension or unease rather than relaxation. While there is a slight smile, it appears inconsistent with the rest of the cues, which point more toward discomfort or forced calmness. Therefore, the smile likely does not reflect genuine relaxation or contentment. | The slight smile, combined with the low pitch, moderate pace, and consistent volume of the speaker's voice, suggests a calm and composed demeanor. Although the eyebrows lower and the forehead wrinkles slightly, which could indicate seriousness or focus, the smile appears genuine and not forced, especially given the context of the phrase "slice 'em up real nice," which may carry a playful or confident tone. Therefore, the smile likely reflects a relaxed and content state rather than tension or discomfort. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: You're gonna slice 'em up real nice.
Speaker face: At the start, the corners of his mouth are pulled down and his eyes are narrowed. By the end, his mouth is open and his eyes are wide.
Tone of voice: The pitch is low and the pace is slow. The voice is strained.
Where the speaker is looking: He is looking to his right.
Speaker body: He is sitting with his hands clasped in front of him.
Other people: not visible
Physical contact: not visible
Other sounds: not audible
Setting: The scene is indoors, in a room with a white brick wall, a chalkboard, and a refrigerator.
```

**v7:**

```
The main speaker is the man in the brown suit jacket. He says, "You're gonna slice 'em up real nice."

The man's mouth opens and closes as he speaks. His lips move to form the words. His eyebrows raise slightly at the beginning of the sentence and lower towards the end. His forehead wrinkles a little as he talks.

The man's hands are clasped together in front of him. His arms remain in the same position throughout the clip. His torso is upright and does not move. His head is turned slightly to his right.

The speaker's voice is of a low pitch. The volume is consistent. The pace is moderate. There is a slight rise in pitch on the word "real."
```
</details>

### `video_150_2` · cue: face · emotions: other · negated
**Fact:** His eyes are slightly crinkled.  
**Correct (A):** The crinkled eyes do not indicate a genuine smile.  
**Other (B):** The crinkled eyes indicate a genuine smile.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is low and the pace is slow. The voice is strained. | The speaker's voice is of a low pitch. The volume is consistent. The pace is moderate. There is a slight rise in pitch on the word "real." |
| Decider's reasoning | The crinkling of the eyes, often referred to as "crow's feet," is a key indicator of a Duchenne smile, which is associated with genuine positive emotion. However, this is contradicted by other cues such as the narrowed eyes, low pitch, strained voice, and slow delivery, which suggest tension or discomfort rather than happiness. Given the overall context, the crinkling may be more consistent with a forced or insincere expression rather than a genuine smile. | The crinkling of the eyes, especially when paired with raised eyebrows and a slight rise in pitch on the word "real," suggests the engagement of the orbicularis oculi muscle, which is typically associated with genuine smiles (Duchenne markers). Although the speaker's tone is low and his hands are clasped, the combination of facial cues leans toward a positive, authentic expression rather than a forced or insincere one. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: You're gonna slice 'em up real nice.
Speaker face: At the start, the corners of his mouth are pulled down and his eyes are narrowed. By the end, his mouth is open and his eyes are wide.
Tone of voice: The pitch is low and the pace is slow. The voice is strained.
Where the speaker is looking: He is looking to his right.
Speaker body: He is sitting with his hands clasped in front of him.
Other people: not visible
Physical contact: not visible
Other sounds: not audible
Setting: The scene is indoors, in a room with a white brick wall, a chalkboard, and a refrigerator.
```

**v7:**

```
The main speaker is the man in the brown suit jacket. He says, "You're gonna slice 'em up real nice."

The man's mouth opens and closes as he speaks. His lips move to form the words. His eyebrows raise slightly at the beginning of the sentence and lower towards the end. His forehead wrinkles a little as he talks.

The man's hands are clasped together in front of him. His arms remain in the same position throughout the clip. His torso is upright and does not move. His head is turned slightly to his right.

The speaker's voice is of a low pitch. The volume is consistent. The pace is moderate. There is a slight rise in pitch on the word "real."
```
</details>

### `video_160_0` · cue: face · emotions: anger, fear/anxiety
**Fact:** He has a tense expression on his face.  
**Correct (A):** The tense expression on his face is a typical sign of anger.  
**Other (B):** The tense expression on his face is a sign of surprise.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | Person B's voice is low and questioning. Person A's voice is higher and sounds like a response. | The speaker's voice is at a medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after the word "this." |
| Decider's reasoning | The man's facial expression includes narrowed eyes, a creased forehead, and drawn eyebrows, which are more consistent with skepticism or intense questioning rather than surprise. Surprise typically involves raised eyebrows and wide eyes, whereas his expression aligns more with tension or anger. Additionally, his low, questioning tone supports a sense of challenge or disbelief rather than astonishment. | The combination of narrowed eyes, furrowed brow, and tense facial muscles often indicates surprise or disbelief rather than anger, especially when paired with a questioning tone and rising intonation. While anger can involve tension, it typically includes more pronounced features like flared nostrils or a rigid jaw, which are not observed here. The slight pause after "this" and the inquisitive nature of the question suggest he is taken aback rather than enraged. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B (man, center of frame, dark suit) is speaking. Person A (woman, right of frame, red sweater) is speaking.
Speech: Person B: "How do you know so much about this?" Person A: [inaudible]
Speaker face: Person B's eyebrows are drawn together, his forehead is creased, his eyes are narrowed, and his mouth is open. His expression remains consistent. Person A's mouth is open and her eyes are wide. Her expression remains consistent.
Tone of voice: Person B's voice is low and questioning. Person A's voice is higher and sounds like a response.
Where the speaker is looking: Person B is looking at Person A. Person A is looking at Person B.
Speaker body: Person B is standing upright. Person A has her arms crossed.
Other people: Person C (man, left of frame, dark suit) is standing with his back to the camera. Person D (woman, right background, dark top) is standing with her hands clasped.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in a room with a textured wall, where people are standing and talking.
```

**v7:**

```
The man in the dark suit is the main speaker. He says, "How do you know so much about this?"

The man's eyebrows move together and down. His forehead wrinkles. His eyes narrow slightly. His mouth opens and closes. His lips move to form words. His cheeks move with his mouth.

The man's torso is mostly still. His head moves slightly. His arms are not visible. His hands are not visible. His legs are not visible.

The speaker's voice is at a medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after the word "this."
```
</details>

### `video_168_1` · cue: face · emotions: intensity/emphasis
**Fact:** The way she stands and the expression on her face.  
**Correct (A):** The way she stands and the expression on her face indicate that she is likely expressing a strong emotion, possibly related to a disagreement or a challenging situation.  
**Other (B):** The way she stands and the expression on her face do not indicate that she is likely expressing a strong emotion, possibly related to a disagreement or a challenging situation.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | Person A's voice is high-pitched and loud. Person B's voice is low-pitched and flat. | The speaker's voice is at a medium pitch. The pitch rises slightly at the end of the first sentence. The voice is loud. The speed is moderate. There are pauses between phrases. The words "special appearance" are said with extra emphasis. |
| Decider's reasoning | Person A's body language—such as her hands on her hips, wide eyes, raised eyebrows, and creased forehead—suggests heightened emotional arousal. Her loud, high-pitched voice and direct gaze toward Person B further support the idea that she is emotionally engaged, possibly in a confrontational or intense moment. These cues align more closely with interpretation A, indicating strong emotion rather than neutrality. | The speaker's facial expressions, such as eyebrow movements, forehead wrinkling, and slight nose flaring, combined with her animated hand and torso movements, suggest active engagement rather than tension or conflict. Her voice is loud and expressive, with emphasis on certain words, indicating enthusiasm or excitement rather than disagreement. These cues align more closely with someone delivering a lively or dramatic announcement than someone in a challenging or confrontational situation. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A's mouth moves while the words are heard. Person B's mouth moves while the words are heard.
Speech: 
Person A: "Oh, I've been waiting so long to get on that body."
Person B: "special appearance by Elliott Gould as Jack Geller"
Person B: "and Christina Pickles as Judy Geller"
Speaker face: At the start, Person A's eyebrows are raised, her forehead is smooth, her eyes are wide, and her mouth is open. At the end, her eyebrows are lowered, her forehead is creased, her eyes are narrowed, and her mouth is open. Person B's face is not visible.
Tone of voice: Person A's voice is high-pitched and loud. Person B's voice is low-pitched and flat.
Where the speaker is looking: Person A is looking at Person B. Person B is looking forward.
Speaker body: Person A's arms are bent at the elbows and her hands are on her hips. Person B's arms are at his sides.
Other people: Person B is wearing a white helmet and a red jacket. He is standing still.
Physical contact: Not applicable.
Other sounds: Not applicable.
Setting: The scene is indoors, in a living room with a yellow couch, a coffee table, and a kitchen area in the background.
```

**v7:**

```
The main speaker is the woman on the left. She says, "special appearance by Elliott Gould as Jack Geller and Christina Pickles as Judy Geller."

The woman's eyebrows move up and down. Her forehead wrinkles and smooths. Her eyes open and close. Her nose flares slightly. Her cheeks move up and down. Her mouth opens and closes. Her lips move.

The woman's arms move. Her hands move. Her torso moves. Her legs move.

The speaker's voice is at a medium pitch. The pitch rises slightly at the end of the first sentence. The voice is loud. The speed is moderate. There are pauses between phrases. The words "special appearance" are said with extra emphasis.
```
</details>

### `video_168_2` · cue: hands/gesture · emotions: anger
**Fact:** The woman is standing with her hands on her hips.  
**Correct (B):** This posture is associated with anger or frustration.  
**Other (A):** This posture is not associated with anger or frustration.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✓ | A ✗ |
| Voice as described | Person A's voice is high-pitched and loud. Person B's voice is low-pitched and flat. | The speaker's voice is at a medium pitch. The pitch rises slightly at the end of the first sentence. The voice is loud. The speed is moderate. There are pauses between phrases. The words "special appearance" are said with extra emphasis. |
| Decider's reasoning | The woman's hands-on-hips posture, combined with her wide eyes, open mouth, and raised eyebrows at the start, suggests heightened emotion. Her voice is loud and high-pitched, and her facial expressions shift to narrowed eyes and a creased forehead by the end, indicating rising tension. These cues align more closely with frustration or anger than with neutral or confident stances. | The woman's hands-on-hips posture is often interpreted as a sign of confidence or assertiveness, especially when combined with her animated facial expressions and energetic delivery. While this stance can sometimes signal frustration, the overall tone of her voice and expressive body language suggest enthusiasm rather than anger. Therefore, interpretation A is more consistent with the observed cues. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A's mouth moves while the words are heard. Person B's mouth moves while the words are heard.
Speech: 
Person A: "Oh, I've been waiting so long to get on that body."
Person B: "special appearance by Elliott Gould as Jack Geller"
Person B: "and Christina Pickles as Judy Geller"
Speaker face: At the start, Person A's eyebrows are raised, her forehead is smooth, her eyes are wide, and her mouth is open. At the end, her eyebrows are lowered, her forehead is creased, her eyes are narrowed, and her mouth is open. Person B's face is not visible.
Tone of voice: Person A's voice is high-pitched and loud. Person B's voice is low-pitched and flat.
Where the speaker is looking: Person A is looking at Person B. Person B is looking forward.
Speaker body: Person A's arms are bent at the elbows and her hands are on her hips. Person B's arms are at his sides.
Other people: Person B is wearing a white helmet and a red jacket. He is standing still.
Physical contact: Not applicable.
Other sounds: Not applicable.
Setting: The scene is indoors, in a living room with a yellow couch, a coffee table, and a kitchen area in the background.
```

**v7:**

```
The main speaker is the woman on the left. She says, "special appearance by Elliott Gould as Jack Geller and Christina Pickles as Judy Geller."

The woman's eyebrows move up and down. Her forehead wrinkles and smooths. Her eyes open and close. Her nose flares slightly. Her cheeks move up and down. Her mouth opens and closes. Her lips move.

The woman's arms move. Her hands move. Her torso moves. Her legs move.

The speaker's voice is at a medium pitch. The pitch rises slightly at the end of the first sentence. The voice is loud. The speed is moderate. There are pauses between phrases. The words "special appearance" are said with extra emphasis.
```
</details>

### `video_208_1` · cue: hands/gesture · emotions: fear/anxiety
**Fact:** Her hands are clasped together in front of her.  
**Correct (B):** This can suggest nervousness or anxiety.  
**Other (A):** This does not suggest nervousness or anxiety.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✓ | A ✗ |
| Voice as described | The pitch is mid-range and steady. The pace is moderate. The voice is clear and the volume is consistent. | The speaker's voice is at a moderate pitch. It rises slightly at the end of the phrase. The pace is moderate. There is a slight pause after the word "No." The word "Phoebe" is spoken with a slightly higher pitch. |
| Decider's reasoning | The clasped hands at the beginning, combined with the initial wide eyes and raised eyebrows, could indicate some level of nervousness or self-protection. However, the person quickly unclasps her hands and begins to gesture openly, which suggests that any initial tension is resolved. Given the overall calm tone and confident delivery, the clasped hands are more likely a momentary posture rather than a sign of ongoing anxiety. | Clasped hands can indicate a range of emotions, but in this context, combined with the slight pause after "No" and the rising pitch on "Phoebe," it may reflect a moment of hesitation or emotional processing. However, her eyes remain focused and her torso is still, which suggests composure rather than overt anxiety. Therefore, the gesture is more likely a sign of thoughtfulness or emphasis than nervousness. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A's mouth moves while the words are heard.
Speech: Person A: "No, I live with Phoebe."
Speaker face: At the start, her eyebrows are slightly raised, her forehead is smooth, her eyes are wide, and her mouth is open. By the end, her eyebrows are lowered, her forehead is creased, her eyes are narrowed, and her mouth is closed.
Tone of voice: The pitch is mid-range and steady. The pace is moderate. The voice is clear and the volume is consistent.
Where the speaker is looking: Person A looks at Person B throughout the clip.
Speaker body: Person A's hands are clasped in front of her. She then unclasps them and gestures with both hands, palms up, moving them outwards and then inwards.
Other people: Person B (man, right of frame, blue sweater) stands still, looking at Person A. His mouth is closed and his expression is neutral.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene takes place in a hallway with a dark green door and beige walls. A woman and a man are standing and talking.
```

**v7:**

```
The woman in the red top is the main speaker. She says, "No, I live with Phoebe."

The woman's eyebrows move slightly upwards and then lower. Her forehead shows some creases. Her eyes remain open and focused. Her mouth opens and closes as she speaks. Her lips move to form words. Her cheeks move with the opening and closing of her mouth.

The woman's hands are clasped together in front of her. She then moves her hands apart and gestures with them. Her arms move slightly as she gestures. Her torso remains mostly still.

The speaker's voice is at a moderate pitch. It rises slightly at the end of the phrase. The pace is moderate. There is a slight pause after the word "No." The word "Phoebe" is spoken with a slightly higher pitch.
```
</details>

### `video_222_2` · cue: hands/gesture · emotions: anger, intensity/emphasis
**Fact:** Her body language includes holding the mug firmly and leaning slightly forward.  
**Correct (A):** Her body language suggests a strong emotional response, which aligns with the emotion of anger.  
**Other (B):** Her body language suggests engagement and enthusiasm, which aligns with the emotion of joy.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is mid-range and steady. The pace is moderate, with a slight emphasis on the word "wouldn't." | The speaker's voice is at a medium pitch. It rises slightly at the end of the first sentence. The pace is moderate, with a brief pause between the two sentences. |
| Decider's reasoning | The person is leaning forward and holding the mug firmly, which can indicate attentiveness and involvement in the conversation. However, her facial expressions shift from wide-eyed and raised eyebrows to a furrowed brow and creased forehead, which are more indicative of concern or skepticism than joy. While the forward lean suggests engagement, the overall expression does not align with the high arousal typically seen in joy or enthusiasm. Therefore, the interpretation involving a strong emotional response like anger is more consistent with the observed tension in her face. | The woman's firm grip on the mug and slight forward lean indicate attentiveness and involvement in the conversation, which are more consistent with engagement and enthusiasm than with anger. Anger typically involves more tension, such as clenched jaws or rigid posture, neither of which are observed here. Her moderate pace, steady tone, and lack of aggressive gestures further support a positive emotional state like joy rather than anger. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: I mean, I could, but I wouldn't.
Speaker face: At the start, her eyebrows are raised and her eyes are wide. By the end, her eyebrows are drawn together and her forehead is creased. Her mouth is open at the start and closes slightly by the end.
Tone of voice: The pitch is mid-range and steady. The pace is moderate, with a slight emphasis on the word "wouldn't."
Where the speaker is looking: She is looking toward the right side of the frame, at another person.
Speaker body: She holds a blue mug with both hands. Her hands move slightly as she speaks.
Other people: Person B (woman, right of frame, purple top) is visible from the side, facing Person A. Person C (man, left of frame, black jacket) is seen from the back, standing with his back to the camera.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in what appears to be a bar or restaurant, with other people in the background.
```

**v7:**

```
The woman in the white shirt is the main speaker. She says, "I mean, I could, but I wouldn't."

The speaker's eyebrows move up and down. Her forehead wrinkles and smooths out. Her eyes look forward and then shift to the side. Her mouth opens and closes, and her lips move to form words. Her cheeks move as she speaks.

The speaker holds a blue mug with both hands. Her arms move slightly as she talks. Her torso remains mostly still. Her hands adjust their grip on the mug.

The speaker's voice is at a medium pitch. It rises slightly at the end of the first sentence. The pace is moderate, with a brief pause between the two sentences.
```
</details>

### `video_236_0` · cue: smile/laugh · emotions: joy · negated
**Fact:** There is a slight smile on his face.  
**Correct (B):** The slight smile does not suggest that he is feeling happy or amused.  
**Other (A):** The slight smile suggests that he is feeling happy or amused.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✓ | A ✗ |
| Voice as described | The pitch is low and the speed is moderate. | The speaker's voice is at a moderate pitch and level. The pace is moderate, with a slight rise in pitch at the end of the sentence. |
| Decider's reasoning | The slight smile is present alongside narrowed eyes and a low-pitched, moderate-speed voice, which often indicates skepticism or disapproval rather than genuine happiness. Additionally, the speaker's statement, “Yeah, I don't think you should say that even when,” conveys disagreement, making it more likely that the smile is not an expression of amusement. Therefore, the smile likely serves as a mask or a sign of controlled emotion rather than genuine joy. | The slight smile, combined with raised cheeks and a relaxed facial expression, typically indicates positive emotion such as amusement or happiness. Although his eyes are looking away and his body is still, the facial cues align more closely with Interpretation A, suggesting genuine positive affect rather than a neutral or forced expression. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: Yeah, I don't think you should say that even when
Speaker face: At the start, the corners of his mouth are pulled up and his eyes are narrowed. At the end, his mouth is open and his eyes are narrowed.
Tone of voice: The pitch is low and the speed is moderate.
Where the speaker is looking: He is looking to his right.
Speaker body: He is sitting with his arms on his knees.
Other people: not visible
Physical contact: not visible
Other sounds: not audible
Setting: The scene is indoors, in a room with a brown leather couch and a large green plant.
```

**v7:**

```
The man in the black shirt is the main speaker. He says, "Yeah, I don't think you should say that even when..."

The man's eyebrows are slightly raised. His forehead is smooth. His eyes are open and looking to his right. His nose is visible. His cheeks are slightly raised. His mouth is open, and his lips move as he speaks.

The man's torso is angled slightly to his left. His arms are resting on his legs. His hands are not visible. His legs are not visible. His body remains mostly still.

The speaker's voice is at a moderate pitch and level. The pace is moderate, with a slight rise in pitch at the end of the sentence.
```
</details>

### `video_236_2` · cue: smile/laugh · emotions: joy, calm/relaxed · negated
**Fact:** There is a slight smile on the speaker's face.  
**Correct (A):** The slight smile does not suggest a relaxed and content expression.  
**Other (B):** The slight smile suggests a relaxed and content expression.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is low and the speed is moderate. | The speaker's voice is at a moderate pitch and level. The pace is moderate, with a slight rise in pitch at the end of the sentence. |
| Decider's reasoning | The slight smile is present alongside narrowed eyes and a low-pitched, moderate-speed voice, which may indicate skepticism or guardedness rather than genuine relaxation or contentment. While smiles can signal positive emotions, the combination of facial tension and vocal tone suggests the smile may be more socially polite or masking underlying discomfort. Therefore, the smile likely does not reflect true relaxation or contentment. | The slight smile, combined with the raised cheeks and open eyes, indicates a genuine and mild positive affect. This expression, along with the smooth forehead and moderate, steady tone, suggests comfort and ease rather than tension or skepticism. Therefore, the smile is more consistent with a relaxed and content state. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: Yeah, I don't think you should say that even when
Speaker face: At the start, the corners of his mouth are pulled up and his eyes are narrowed. At the end, his mouth is open and his eyes are narrowed.
Tone of voice: The pitch is low and the speed is moderate.
Where the speaker is looking: He is looking to his right.
Speaker body: He is sitting with his arms on his knees.
Other people: not visible
Physical contact: not visible
Other sounds: not audible
Setting: The scene is indoors, in a room with a brown leather couch and a large green plant.
```

**v7:**

```
The man in the black shirt is the main speaker. He says, "Yeah, I don't think you should say that even when..."

The man's eyebrows are slightly raised. His forehead is smooth. His eyes are open and looking to his right. His nose is visible. His cheeks are slightly raised. His mouth is open, and his lips move as he speaks.

The man's torso is angled slightly to his left. His arms are resting on his legs. His hands are not visible. His legs are not visible. His body remains mostly still.

The speaker's voice is at a moderate pitch and level. The pace is moderate, with a slight rise in pitch at the end of the sentence.
```
</details>

### `video_249_0` · cue: smile/laugh · emotions: other
**Fact:** The man is smiling.  
**Correct (A):** His smile indicates that he is enjoying the interaction with the woman.  
**Other (B):** His smile is a facade to mask his anger.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | Person A's voice is high-pitched, loud, fast, with a rising inflection. Person B's voice is high-pitched, loud, fast, with a rising inflection. | The speaker's voice is low and steady. The pitch is consistent. The pace is moderate. There are no noticeable pauses or changes in loudness. |
| Decider's reasoning | The man's smile is accompanied by raised cheeks and a wrinkled nose, which are indicators of a genuine Duchenne smile. His open posture, leaning forward, and physical contact (hands on the woman's stomach) suggest warmth and engagement. These cues align more with genuine enjoyment than masking anger, which would likely involve tense facial muscles or conflicting body language. | The man's facial expressions, such as narrowed eyes, flared nose, and forehead wrinkles, suggest tension or concern rather than genuine enjoyment. While he is smiling, the combination of these tense facial cues and his forward-leaning posture—often associated with urgency or confrontation—implies the smile may be masking underlying frustration or anger. His steady, low voice and lack of pauses suggest controlled emotion, which supports the idea of a restrained or forced expression. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A's mouth moves while the words are heard. Person B's mouth moves while the words are heard. Person A is speaking.
Speech: Person A: "You okay? What's wrong?" Person B: "I'm fine."
Speaker face: Person A's eyebrows are raised, forehead is smooth, eyes are wide, mouth corners are up, cheeks are raised, nose is wrinkled. Person B's eyebrows are raised, forehead is smooth, eyes are wide, mouth corners are up, cheeks are raised, nose is wrinkled.
Tone of voice: Person A's voice is high-pitched, loud, fast, with a rising inflection. Person B's voice is high-pitched, loud, fast, with a rising inflection.
Where the speaker is looking: Person A is looking at Person B. Person B is looking at Person A.
Speaker body: Person A is leaning forward, arms are open. Person B is lying down, arms are open.
Other people: Person B's face is visible. Person B is looking at Person A. Person B's posture is reclined. Person B's hands are on Person A's arms.
Physical contact: Person A's hands are on Person B's stomach. Person B's hands are on Person A's arms.
Other sounds: Not audible.
Setting: The scene is indoors, on a couch, with two people interacting.
```

**v7:**

```
The man in the blue shirt is the main speaker. He says, "You okay? What's wrong?"

The man's eyebrows move together and then apart. His forehead wrinkles slightly. His eyes narrow and then open wider. His nose flares a little. His cheeks rise. His mouth opens and closes, and his lips move to form words.

The man's arms are bent and his hands are on the woman's stomach. His legs are bent and his feet are on the floor. His torso is leaning forward.

The speaker's voice is low and steady. The pitch is consistent. The pace is moderate. There are no noticeable pauses or changes in loudness.
```
</details>

### `video_249_1` · cue: smile/laugh · emotions: joy
**Fact:** The man is smiling.  
**Correct (B):** His smile suggests that he is feeling joy.  
**Other (A):** His smile does not suggest that he is feeling joy.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✓ | A ✗ |
| Voice as described | Person A's voice is high-pitched, loud, fast, with a rising inflection. Person B's voice is high-pitched, loud, fast, with a rising inflection. | The speaker's voice is low and steady. The pitch is consistent. The pace is moderate. There are no noticeable pauses or changes in loudness. |
| Decider's reasoning | The man's smile is accompanied by raised cheeks and a wrinkled nose, which are indicators of a genuine smile (Duchenne smile). Additionally, his wide eyes, open posture, and forward lean suggest engagement and concern rather than false positivity. These cues align more with authentic emotional expression than masking true feelings. | The man's smile is accompanied by raised cheeks and a slight opening of the mouth, which are typical indicators of a genuine smile. However, his eyebrows are moving together and his forehead wrinkles slightly, which may suggest concern or concentration. Given that he is asking, "You okay? What's wrong?" in a low, steady voice, his smile likely reflects empathy or reassurance rather than joy. Therefore, the smile appears to be more about concern than happiness. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A's mouth moves while the words are heard. Person B's mouth moves while the words are heard. Person A is speaking.
Speech: Person A: "You okay? What's wrong?" Person B: "I'm fine."
Speaker face: Person A's eyebrows are raised, forehead is smooth, eyes are wide, mouth corners are up, cheeks are raised, nose is wrinkled. Person B's eyebrows are raised, forehead is smooth, eyes are wide, mouth corners are up, cheeks are raised, nose is wrinkled.
Tone of voice: Person A's voice is high-pitched, loud, fast, with a rising inflection. Person B's voice is high-pitched, loud, fast, with a rising inflection.
Where the speaker is looking: Person A is looking at Person B. Person B is looking at Person A.
Speaker body: Person A is leaning forward, arms are open. Person B is lying down, arms are open.
Other people: Person B's face is visible. Person B is looking at Person A. Person B's posture is reclined. Person B's hands are on Person A's arms.
Physical contact: Person A's hands are on Person B's stomach. Person B's hands are on Person A's arms.
Other sounds: Not audible.
Setting: The scene is indoors, on a couch, with two people interacting.
```

**v7:**

```
The man in the blue shirt is the main speaker. He says, "You okay? What's wrong?"

The man's eyebrows move together and then apart. His forehead wrinkles slightly. His eyes narrow and then open wider. His nose flares a little. His cheeks rise. His mouth opens and closes, and his lips move to form words.

The man's arms are bent and his hands are on the woman's stomach. His legs are bent and his feet are on the floor. His torso is leaning forward.

The speaker's voice is low and steady. The pitch is consistent. The pace is moderate. There are no noticeable pauses or changes in loudness.
```
</details>

### `video_267_0` · cue: voice/speech · emotions: joy · negated
**Fact:** The speaker is gesturing with open hands.  
**Correct (A):** The open hand gestures do not suggest the speaker is feeling joy.  
**Other (B):** The open hand gestures suggest the speaker is feeling joy.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is mid-range and the pace is moderate. The voice is clear and steady. | Her voice is at a medium pitch. It rises and falls. It is spoken at a moderate speed. There are pauses between phrases. The words "comes to the wedding" are said with extra emphasis. |
| Decider's reasoning | Open hand gestures often indicate openness, honesty, or a desire to connect, but they are not exclusive to joy. Given the speaker’s clear, steady voice and moderate pace, her tone seems neutral to positive, but there is no strong evidence of joy in her facial expressions—her eyebrows lower by the end, and her mouth closes. The gestures may instead reflect a conversational openness rather than emotional joy. | Open hand gestures often indicate openness, honesty, and positive emotions such as joy or enthusiasm. Given that the speaker emphasizes the phrase "comes to the wedding" with vocal inflection and uses expressive facial movements, the open hands likely reinforce a sense of warmth and excitement rather than neutrality or negativity. Therefore, the gesture aligns more closely with expressing joy. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A (woman, left of frame, red sweater)
Speech: And so she comes to the wedding.
Speaker face: At the start, her eyebrows are raised and her mouth is open. By the end, her eyebrows are lowered and her mouth is closed.
Tone of voice: The pitch is mid-range and the pace is moderate. The voice is clear and steady.
Where the speaker is looking: She looks toward Person B (man, right of frame, red sweater) and then turns her head slightly to the left.
Speaker body: She stands with her arms slightly bent and hands open, gesturing outward. She then lowers her hands to her sides.
Other people: Person B (man, right of frame, red sweater) stands with his back mostly to the camera, facing Person A. He remains still.
Physical contact: No physical contact occurs.
Other sounds: Not audible.
Setting: The scene is set in a kitchen and living room area, with a refrigerator, table, and couch visible.
```

**v7:**

```
The main speaker is the woman in the pink shirt. She says, "And so she comes to the wedding."

Her eyebrows move up and down. Her forehead wrinkles and smooths. Her eyes open and close. Her mouth opens and closes. Her lips move and change shape. Her cheeks move.

Her arms move. Her hands move. Her torso moves. Her legs move.

Her voice is at a medium pitch. It rises and falls. It is spoken at a moderate speed. There are pauses between phrases. The words "comes to the wedding" are said with extra emphasis.
```
</details>

### `video_280_1` · cue: face · emotions: intensity/emphasis
**Fact:** His mouth is open.  
**Correct (A):** His mouth being open suggests he is shouting or speaking forcefully.  
**Other (B):** His mouth being open does not suggest that he is shouting or speaking forcefully.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is high and the volume is loud. The speech is fast and forceful, with the words "not" and "Rachel" emphasized. | The speaker's voice is low. It rises at the end of the sentence. The pace is moderate. There is a pause after "Rachel." The word "okay" is said with emphasis. |
| Decider's reasoning | The speaker's mouth is open at the end of his speech, which aligns with his loud, forceful, and high-pitched delivery. Given that he emphasizes key words and speaks quickly, the open mouth is consistent with an intense, emotionally charged tone rather than a neutral or calm one. Therefore, the open mouth supports the interpretation that he is speaking forcefully. | The speaker's voice is described as low and his pace is moderate, with no indication of raised volume. Although his mouth is open, the emphasis on "okay" and the controlled hand movements suggest he is trying to assert himself without shouting. The open mouth is more likely a result of deliberate articulation than forceful speech. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B (man, right of frame, green t-shirt)
Speech: I do not have feelings for Rachel, okay?
Speaker face: At the start, the corners of his mouth are pulled down and his eyes are narrowed. At the end, his mouth is open and his eyes are wide.
Tone of voice: The pitch is high and the volume is loud. The speech is fast and forceful, with the words "not" and "Rachel" emphasized.
Where the speaker is looking: He is looking at Person A and turns his head slightly toward her.
Speaker body: He is standing upright with his left arm bent and hand on his shoulder. His right hand moves in a small gesture.
Other people: Person A (woman, left of frame, red sweater) is looking at Person B. Her face is not visible.
Physical contact: Not applicable.
Other sounds: Not applicable.
Setting: The scene is indoors, in a hallway with a green door marked "20". A man and a woman are having a conversation.
```

**v7:**

```
The man in the green t-shirt is the main speaker. He says, "I do not have feelings for Rachel, okay?"

The man's eyebrows move up and down. His forehead wrinkles. His eyes look toward the woman. His nose flares slightly. His cheeks move. His mouth opens and closes. His lips press together and then part.

The man's left arm holds a grey jacket. His right hand moves up and down. His right hand moves side to side. His torso shifts slightly.

The speaker's voice is low. It rises at the end of the sentence. The pace is moderate. There is a pause after "Rachel." The word "okay" is said with emphasis.
```
</details>

### `video_282_2` · cue: face · emotions: anger
**Fact:** Her mouth movements suggest she is speaking with intensity.  
**Correct (A):** The mouth movements indicate she is possibly feeling frustration.  
**Other (B):** The mouth movements do not indicate that she is possibly feeling frustration.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is high and the pace is fast. The voice is strained and the words are spoken with emphasis. | The speaker's voice is high-pitched. It rises and falls. The pace is moderate. There are short pauses between phrases. The word "good" is said with emphasis. |
| Decider's reasoning | The combination of intense mouth movements, a strained voice, and facial tension (such as furrowed brows and narrowed eyes) suggests emotional intensity. While the mouth shape at the end of the clip (corners pulled down) could indicate frustration, the overall context of high pitch, fast pace, and emphatic delivery points more toward passion or urgency than frustration. Therefore, the evidence supports that her mouth movements are consistent with strong emotion, possibly frustration, but not definitively ruling it out. | The speaker's mouth movements, combined with her high-pitched voice, emphasis on the word "good," and animated hand gestures, suggest she is passionately conveying her message rather than expressing frustration. While her facial expressions are dynamic, they align more with emotional engagement than irritation. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A (woman, left of frame, red sweater)
Speech: [inaudible]
Speaker face: At the start, her eyebrows are drawn together, her forehead is creased, her eyes are narrowed, and her mouth is open. At the end, her eyebrows are raised, her forehead is smooth, her eyes are wide, and her mouth is open with the corners pulled down.
Tone of voice: The pitch is high and the pace is fast. The voice is strained and the words are spoken with emphasis.
Where the speaker is looking: She looks down at her hands, then looks up and to her right, and then looks up and to her left.
Speaker body: She moves her hands in a circular motion in front of her chest, then raises her right hand and points her index finger up and down. She then raises her left hand and points her index finger up and down.
Other people: not visible
Physical contact: not visible
Other sounds: not audible
Setting: The scene is indoors, in a kitchen. A woman is standing and talking.
```

**v7:**

```
The main speaker is the woman in the dark coat. She says, "No, no, the kiss was good."

The woman's eyebrows move up and down. Her forehead wrinkles and smooths out. Her eyes open and close slightly. Her mouth opens and closes, and her lips move. Her cheeks move in and out.

The woman raises her hands and moves them in front of her. She points with her right hand. Her left hand moves up and down. Her torso shifts slightly.

The speaker's voice is high-pitched. It rises and falls. The pace is moderate. There are short pauses between phrases. The word "good" is said with emphasis.
```
</details>

### `video_282_3` · cue: gaze · emotions: anger, intensity/emphasis
**Fact:** She is making direct eye contact.  
**Correct (A):** Making direct eye contact is a common indicator of anger or strong emotion.  
**Other (B):** Making direct eye contact is a sign of confidence and engagement, often associated with positive emotions like joy.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is high and the pace is fast. The voice is strained and the words are spoken with emphasis. | The speaker's voice is high-pitched. It rises and falls. The pace is moderate. There are short pauses between phrases. The word "good" is said with emphasis. |
| Decider's reasoning | The speaker's facial expressions and vocal tone suggest high emotional intensity, including tension and strain, which aligns more closely with strong emotions like anger rather than joy. While direct eye contact can indicate confidence, the combination of furrowed brows, narrowed eyes, and a strained voice points toward a negative emotional state. Therefore, interpretation A is more consistent with the observed cues. | The woman's overall body language, including her animated facial expressions, hand gestures, and high-pitched, expressive voice, suggests she is emotionally engaged and conveying a positive sentiment. Her emphasis on the word "good" and the lively movement of her face and hands align more closely with enthusiasm or joy rather than anger. Therefore, interpretation B is more consistent with the observed cues. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A (woman, left of frame, red sweater)
Speech: [inaudible]
Speaker face: At the start, her eyebrows are drawn together, her forehead is creased, her eyes are narrowed, and her mouth is open. At the end, her eyebrows are raised, her forehead is smooth, her eyes are wide, and her mouth is open with the corners pulled down.
Tone of voice: The pitch is high and the pace is fast. The voice is strained and the words are spoken with emphasis.
Where the speaker is looking: She looks down at her hands, then looks up and to her right, and then looks up and to her left.
Speaker body: She moves her hands in a circular motion in front of her chest, then raises her right hand and points her index finger up and down. She then raises her left hand and points her index finger up and down.
Other people: not visible
Physical contact: not visible
Other sounds: not audible
Setting: The scene is indoors, in a kitchen. A woman is standing and talking.
```

**v7:**

```
The main speaker is the woman in the dark coat. She says, "No, no, the kiss was good."

The woman's eyebrows move up and down. Her forehead wrinkles and smooths out. Her eyes open and close slightly. Her mouth opens and closes, and her lips move. Her cheeks move in and out.

The woman raises her hands and moves them in front of her. She points with her right hand. Her left hand moves up and down. Her torso shifts slightly.

The speaker's voice is high-pitched. It rises and falls. The pace is moderate. There are short pauses between phrases. The word "good" is said with emphasis.
```
</details>

### `video_286_1` · cue: face · emotions: intensity/emphasis
**Fact:** Her mouth movements are firm and deliberate.  
**Correct (A):** Her mouth movements indicate a strong emotional response.  
**Other (B):** Her mouth movements do not indicate a strong emotional response.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is high and the pace is fast. The voice is strained and loud. | The speaker's voice is high. It rises and falls. The pace is moderate. There are pauses between phrases. The words "wait a minute" and "all the words" are emphasized. |
| Decider's reasoning | The speaker's firm and deliberate mouth movements, combined with her wide eyes, high-pitched and loud voice, and fast speech pace, suggest she is emotionally charged. These cues align more closely with a strong emotional response rather than a neutral or controlled one. Therefore, interpretation A is more consistent with the overall body language and vocal tone. | The speaker's mouth movements are described as firm and deliberate, which suggests control and intentionality rather than uncontrolled emotional expression. While her voice is high and she emphasizes certain phrases, the deliberate nature of her mouth movements aligns more closely with purposeful communication than with a strong emotional reaction. Therefore, the movements likely reflect emphasis or clarity rather than emotional intensity. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B
Speech: Now wait a minute. You just took all the words.
Speaker face: At the start, her eyebrows are raised and her eyes are wide. By the end, her eyebrows are lowered and her eyes are narrowed.
Tone of voice: The pitch is high and the pace is fast. The voice is strained and loud.
Where the speaker is looking: She looks toward Person A, then turns her head to look up and to her right.
Speaker body: She stands with her arms at her sides, then raises her right arm and points upward.
Other people: Person A (woman, left of frame, pink sweater) is sitting on a couch. She stands up, turns to face Person B, and raises her hands.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is in a furnished living room where two women are having a conversation.
```

**v7:**

```
The main speaker is the woman in the black sweater. She says, "Now wait a minute. You just took all the words."

The speaker's mouth opens wide and moves as she speaks. Her eyebrows raise and lower. Her forehead wrinkles slightly. Her eyes look forward. Her cheeks move as she talks. Her lips stretch and contract.

The speaker raises her right hand. She moves her hand up and down. She then raises her left hand. She moves her left hand up and down.

The speaker's voice is high. It rises and falls. The pace is moderate. There are pauses between phrases. The words "wait a minute" and "all the words" are emphasized.
```
</details>

### `video_378_1` · cue: smile/laugh · emotions: joy
**Fact:** The man is smiling.  
**Correct (A):** The smiling indicates a positive and happy emotion.  
**Other (B):** The smiling is a nervous or anxious response to fear.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | The pitch is medium. The pace is moderate. The voice is clear. | The speaker's voice is low. The pitch is steady. The loudness is moderate. The speed is normal. There are no noticeable pauses or emphasis. |
| Decider's reasoning | The man is smiling while looking down and touching his nose and cheek, which are common self-soothing gestures. His body language does not show signs of distress or fear, such as wide eyes or tense muscles. Instead, the smile appears genuine and relaxed, suggesting a positive emotional state rather than nervousness. | The man's eyebrows are raised and his forehead is wrinkled, which can indicate tension or concern. While his cheeks are raised (a sign of smiling), the partial eye closure and low, steady voice suggest he may be masking discomfort. The hand touching his face and slight torso turn further support a defensive or uneasy posture, making the smile appear more nervous than genuinely happy. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: Oh, there you go.
Speaker face: The corners of her mouth are pulled up. Her eyes are narrowed. Her head is tilted down and to her right.
Tone of voice: The pitch is medium. The pace is moderate. The voice is clear.
Where the speaker is looking: Down and to her right.
Speaker body: Her right hand is raised to her face, touching her nose and cheek. Her left hand is resting on a surface in front of her.
Other people: Person B (man, wearing a dark cap and glasses) is standing in profile to the left of the frame. He is smiling and looking down. His right hand is raised to his face, touching his nose and cheek. He lowers his hand and turns his head slightly to the left.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in a kitchen with shelves of food and hanging pots.
```

**v7:**

```
The main speaker is the man in the dark blue fleece jacket and baseball cap. He says, "Oh, there you are."

The man's eyebrows are slightly raised. His forehead is wrinkled. His eyes are partially closed. His nose is visible. His cheeks are raised. His mouth is open and his lips are moving.

The man's right hand is touching his face. His left arm is bent. His torso is slightly turned. His head is tilted.

The speaker's voice is low. The pitch is steady. The loudness is moderate. The speed is normal. There are no noticeable pauses or emphasis.
```
</details>

### `video_383_3` · cue: face · emotions: intensity/emphasis
**Fact:** She is speaking with a stern and intense expression.  
**Correct (B):** She appears to be speaking with a stern and intense expression.  
**Other (A):** She does not appear to be speaking with a stern and intense expression.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✓ | A ✗ |
| Voice as described | The pitch is mid-range and the pace is moderate. The voice is breathy and the words are spoken with a slight upward inflection at the end. | Her voice is at a medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after "No." The word "fun" is spoken with a slightly higher pitch. |
| Decider's reasoning | The observations show that Person A's eyebrows are lowered and her eyes are narrowed by the end, which are classic indicators of a stern or intense expression. Although her initial facial cues were more open and surprised, the progression of her expression toward the end aligns more closely with interpretation B. The breathy voice and slight upward inflection may suggest hesitation or uncertainty, but the dominant visual cues support the idea of intensity. | The speaker's eyebrows are moving slightly up and down, and her forehead shows small wrinkles, which can indicate tension or focus. However, her eyes shift to the side and her mouth moves naturally with speech, suggesting a more casual or playful tone rather than sternness. The slight pause after "No" and the higher pitch on "fun" further imply lightheartedness rather than intensity. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: I just thought it would be fun.
Speaker face: At the start, her eyebrows are slightly raised and her eyes are wide. By the end, her eyebrows are lowered and her eyes are narrowed. Her mouth is slightly open at the start and closes by the end.
Tone of voice: The pitch is mid-range and the pace is moderate. The voice is breathy and the words are spoken with a slight upward inflection at the end.
Where the speaker is looking: She is looking at Person B.
Speaker body: She is standing with her arms at her sides and her body facing Person B.
Other people: Person B is standing to the right of the frame, facing Person A. His face is partially visible. He is wearing a blue shirt with a pattern on it.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in a room with framed pictures on the wall and a mirror. Person A and Person B are standing and talking to each other.
```

**v7:**

```
The main speaker is the woman in the red dress. She says, "No, I just thought it would be fun."

Her eyebrows move slightly up and down. Her forehead shows small wrinkles. Her eyes look forward and then shift to the side. Her mouth opens and closes, and her lips move with the words.

Her arms are at her sides. Her hands are not visible. Her torso is still. Her shoulders are level.

Her voice is at a medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after "No." The word "fun" is spoken with a slightly higher pitch.
```
</details>

### `video_393_1` · cue: face · emotions: anger, sadness, fear/anxiety
**Fact:** The man has raised eyebrows and a tense posture.  
**Correct (A):** His body language, including raised eyebrows and a tense posture, suggests that he is upset or frustrated about something.  
**Other (B):** His body language, including raised eyebrows and a tense posture, does not suggest that he is upset or frustrated about something.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✓ | B ✗ |
| Voice as described | Person A's voice is loud and strained. Person B's voice is lower and calmer. | The speaker's voice is low and steady. The pace is moderate. There are slight pauses between phrases. The words "one girl" are spoken with a slightly lower pitch. |
| Decider's reasoning | The man's tense posture and raised eyebrows, combined with his loud and strained voice, indicate emotional intensity. These cues align more closely with signs of frustration or upset rather than calmness or neutrality. Therefore, interpretation A is more consistent with the observed body language and vocal tone. | The raised eyebrows and forehead wrinkles indicate heightened attention or emphasis, not necessarily distress. His voice remains low and steady, and his torso is mostly still, which contradicts signs of frustration. The slight pauses and controlled pace suggest he is carefully choosing his words rather than being upset. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A's mouth moves while the words are heard. Person B's mouth moves while the words are heard. Person A is speaking.
Speech: Person A: "Well, that's all right, sir, and that's just one girl."
Person B: [inaudible]
Speaker face: Person A's mouth is open. Person B's mouth is closed. Person B's mouth opens.
Tone of voice: Person A's voice is loud and strained. Person B's voice is lower and calmer.
Where the speaker is looking: Person A looks at Person B. Person B looks at Person A.
Speaker body: Person A holds a glass with a straw in his left hand. Person B raises his right hand and points his index finger.
Other people: Person A holds a glass with a straw in his left hand. Person B raises his right hand and points his index finger.
Physical contact: Person B raises his right hand and points his index finger.
Other sounds: Not audible.
Setting: The scene is indoors, in a dimly lit bar or club, with people sitting at tables.
```

**v7:**

```
The man on the left is the main speaker. He says, "Well, that's all right, sir, and that's just one girl."

The man on the left's mouth opens wide and moves as he speaks. His eyebrows raise and lower. His forehead wrinkles. His eyes look forward and then shift to the right. His cheeks move with his mouth. His lips stretch and relax.

The man on the left holds a glass in his right hand. His left hand rests on the table. His torso remains mostly still. His head turns slightly to the right.

The speaker's voice is low and steady. The pace is moderate. There are slight pauses between phrases. The words "one girl" are spoken with a slightly lower pitch.
```
</details>

## v7 right, v3 wrong (20)

### `video_76_0` · cue: hands/gesture · emotions: intensity/emphasis, engagement/attention
**Fact:** The man is gesturing with his hands.  
**Correct (B):** The gesturing suggests he is engaged and passionate about what he is saying.  
**Other (A):** The gesturing does not suggest he is engaged and passionate about what he is saying.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | The voice is low, the pace is slow, and the words are spoken with a strained quality. | The speaker's voice is of a medium pitch. It is spoken at a moderate speed. There are slight pauses between phrases. The words "good lie" are spoken with a slightly lower pitch. |
| Decider's reasoning | The man's hands are held up in front of him with arms slightly bent, and his voice is low, slow, and strained—qualities that suggest internal tension rather than outward enthusiasm. While he is gesturing, the overall body language (narrowed eyes, downturned mouth, and tense delivery) conveys discomfort or seriousness, not passion. Therefore, the gesture likely reflects emotional strain rather than engagement or excitement. | The man's hand gestures, combined with his body turning toward the woman and his facial expressions like raised eyebrows and forehead wrinkles, indicate active involvement in the conversation. These cues typically signal emotional investment and emphasis, which aligns more with passion and engagement than disinterest. Therefore, the gesturing likely reflects his emotional connection to the topic. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person C (man, right of frame, red sweater)
Speech: I need a good lie.
Speaker face: At the start, the corners of his mouth are pulled down and his eyes are narrowed. At the end, his mouth is open and his eyes are wide.
Tone of voice: The voice is low, the pace is slow, and the words are spoken with a strained quality.
Where the speaker is looking: He is looking at Person A.
Speaker body: He is standing with his arms slightly bent and his hands held up in front of him.
Other people: Person A (woman, left of frame, red sweater) is standing with her arms at her sides, looking at Person C. Person B (man, center of frame, black shirt) is standing with his arms at his sides, looking at Person C.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is in a kitchen with a dining table, chairs, and shelves filled with dishes.
```

**v7:**

```
The main speaker is the man in the red sweater. He says, "I need a good lie."

The man in the red sweater's mouth opens and closes as he speaks. His lips move to form the words. His eyebrows raise slightly as he talks. His forehead shows some wrinkles when he speaks.

The man in the red sweater holds a box in his hands. He gestures with his hands while talking. His body turns towards the woman in the brown skirt. His arms move as he speaks.

The speaker's voice is of a medium pitch. It is spoken at a moderate speed. There are slight pauses between phrases. The words "good lie" are spoken with a slightly lower pitch.
```
</details>

### `video_84_1` · cue: smile/laugh · emotions: joy
**Fact:** The woman is smiling.  
**Correct (A):** Her facial expressions suggest that she is in a cheerful and happy mood.  
**Other (B):** Her smile is likely masking her feelings of disgust.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✗ | A ✓ |
| Voice as described | The pitch is mid-range and the pace is moderate. The voice is clear and steady. | The speaker's voice is at a moderate pitch. The pace is steady and the volume is consistent. There are no noticeable pauses or changes in emphasis. |
| Decider's reasoning | The speaker's mouth is pulled up in a smile, but her eyes are narrowed, which can indicate a Duchenne vs. non-Duchenne smile. Since the eyes are narrowed and not relaxed or crinkled at the corners, this suggests the smile may not be genuine. Combined with her body language—looking away, shifting weight, and holding a pole—she may be trying to appear friendly while feeling uncomfortable or displeased. This supports the idea that the smile is masking negative emotions like disgust. | The woman's smile is accompanied by raised cheeks and open, focused eyes, which are consistent with genuine positive emotion. Her steady tone, moderate pitch, and lack of vocal tension further support the interpretation that her smile reflects a cheerful mood rather than concealed disgust. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: I'm just cleaning up.
Speaker face: At the start, the corners of her mouth are pulled up and her eyes are narrowed. At the end, her mouth is open and her eyes are narrowed.
Tone of voice: The pitch is mid-range and the pace is moderate. The voice is clear and steady.
Where the speaker is looking: She is looking towards the right of the frame.
Speaker body: She is standing with her body angled slightly to the right. She holds a blue pole with both hands and shifts her weight from one foot to the other.
Other people: not visible
Physical contact: not visible
Other sounds: not audible
Setting: The scene is indoors, in what appears to be a bar or cafe, with a woman standing behind the counter.
```

**v7:**

```
The main speaker is the woman in the foreground. She says, "I'm just cleaning up."

The woman's mouth opens and closes as she speaks. Her lips move to form the words. Her cheeks rise slightly as she talks. Her eyes remain open and focused forward.

The woman holds a blue object in her hands. Her arms are bent at the elbows. Her torso is upright. Her legs are together and stationary.

The speaker's voice is at a moderate pitch. The pace is steady and the volume is consistent. There are no noticeable pauses or changes in emphasis.
```
</details>

### `video_94_0` · cue: voice/speech · emotions: anger
**Fact:** The speaker appears to be kneeling next to the person on the floor.  
**Correct (B):** Their body language suggests that they are confrontational and possibly frustrated with the situation involving the person on the floor.  
**Other (A):** Their body language suggests that they are concerned and possibly worried about the person on the floor.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | High-pitched, loud, and fast-paced. | The speaker's voice is high-pitched and loud. She speaks quickly with little pause between words. Her voice rises in pitch at the end of the phrase. |
| Decider's reasoning | The speaker’s high-pitched, loud, and fast-paced tone, combined with leaning forward and holding the other person’s legs, suggests urgency or emotional intensity. However, the open mouth and raised eyebrows at the start, along with the forward-leaning posture and physical contact, indicate engagement and concern rather than aggression. The lack of hostile gestures and the attentive gaze toward the other person support a caring interpretation over a confrontational one. | The speaker's wide-open mouth, raised eyebrows, and wrinkled forehead suggest heightened emotional arousal, but the combination with a high-pitched, loud, and fast-paced voice—along with the forward lean and hands on the other person's legs—points more toward urgency or excitement than aggression. While concern could be a possibility, the vocal tone and physical intensity lean more toward a confrontational or demanding stance rather than gentle reassurance. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B
Speech: [inaudible]
Speaker face: At the start, her eyebrows are raised and her mouth is open. At the end, her eyebrows are drawn together and her mouth is open wider.
Tone of voice: High-pitched, loud, and fast-paced.
Where the speaker is looking: She is looking at Person A.
Speaker body: She is kneeling on the floor, leaning forward, and holding Person A's legs.
Other people: Person A is lying on her back, then rolls onto her stomach, and then pushes herself forward on her hands and knees. She is looking at Person B.
Physical contact: Person B is holding Person A's legs.
Other sounds: Not audible.
Setting: The scene is in a living room with a couch, coffee table, and rug. Two women are on the floor.
```

**v7:**

```
The main speaker is the woman in the light green shirt. She says, "I'm turning it on."

The woman in the green shirt's mouth opens wide as she speaks. Her eyebrows raise and her forehead wrinkles. Her eyes narrow slightly and her cheeks move as she talks. Her lips stretch and pull back as she forms the words.

The woman in the green shirt keeps her hands on the other woman's legs. She shifts her weight slightly on the floor. Her torso remains mostly still as she leans forward. Her arms stay bent and close to her body.

The speaker's voice is high-pitched and loud. She speaks quickly with little pause between words. Her voice rises in pitch at the end of the phrase.
```
</details>

### `video_99_0` · cue: hands/gesture · emotions: intensity/emphasis
**Fact:** The man is gesturing with his hands.  
**Correct (A):** His gesturing suggests that he is expressing strong emotions.  
**Other (B):** His gesturing does not suggest that he is expressing strong emotions.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✗ | A ✓ |
| Voice as described | The pitch is mid-range and the pace is moderate. The voice is clear and steady. | The speaker's voice is low. It rises and falls. It is loud. It is fast. He emphasizes the words "Ross" and "going." |
| Decider's reasoning | The man’s gestures—raising both hands and pointing with his index fingers—are deliberate and synchronized with his speech, indicating emphasis rather than emotional intensity. His facial expressions, such as wide eyes and a steady voice, suggest engagement and clarity rather than heightened emotion. Therefore, the gestures appear to serve a communicative function rather than signaling strong feelings. | The man's hand gestures, combined with dynamic facial expressions like eyebrow movements, forehead wrinkling, and mouth changes, indicate active engagement and emotional expression. His voice also varies in pitch and speed, emphasizing key words, which supports the idea that he is conveying strong emotions. Therefore, the gestures are likely reinforcing his emotional state rather than being neutral or restrained. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A (man, right of frame, grey suit)
Speech: Well then to quote Ross, I better be going.
Speaker face: At the start, the corners of his mouth are pulled up and his eyes are wide. At the end, his mouth is open and his eyes are wide.
Tone of voice: The pitch is mid-range and the pace is moderate. The voice is clear and steady.
Where the speaker is looking: He is looking at Person B.
Speaker body: His arms are at his sides. He raises his right hand and points with his index finger, then raises his left hand and points with his index finger.
Other people: Person B (woman, left of frame, black top) has her back to the camera. She is standing still.
Physical contact: Not applicable.
Other sounds: Not applicable.
Setting: The scene is indoors, in a kitchen. A man and a woman are standing and talking.
```

**v7:**

```
The man in the grey suit is the main speaker. He says, "Well then to quote Ross, I better be going."

The man's eyebrows raise and lower. His forehead wrinkles. His eyes open and close. His nose flares. His cheeks move. His mouth opens and closes. His lips purse and stretch.

The man's arms move. His hands gesture. His torso shifts.

The speaker's voice is low. It rises and falls. It is loud. It is fast. He emphasizes the words "Ross" and "going."
```
</details>

### `video_160_3` · cue: gaze · emotions: other
**Fact:** The man has an open mouth and direct gaze.  
**Correct (B):** His open mouth and direct gaze suggest he is making a point or explaining something.  
**Other (A):** His open mouth and direct gaze do not suggest that he is making a point or explaining something.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | Person B's voice is low and questioning. Person A's voice is higher and sounds like a response. | The speaker's voice is at a medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after the word "this." |
| Decider's reasoning | The man's open mouth and direct gaze, combined with his questioning tone and consistent facial expression, indicate he is actively engaged in a conversation and seeking clarification rather than making a declarative statement. While his posture is upright and his expression is intense, the context of his question ("How do you know so much about this?") suggests he is challenging or probing, not explaining or asserting. Therefore, the interpretation that he is not making a point or explaining something aligns better with the observed cues. | The man's open mouth and direct gaze, combined with his questioning tone and raised eyebrows, indicate active engagement and a desire to understand or challenge. These cues are more consistent with someone seeking clarification or making a point than with passive listening. Therefore, the interpretation that he is making a point or explaining something is more fitting. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B (man, center of frame, dark suit) is speaking. Person A (woman, right of frame, red sweater) is speaking.
Speech: Person B: "How do you know so much about this?" Person A: [inaudible]
Speaker face: Person B's eyebrows are drawn together, his forehead is creased, his eyes are narrowed, and his mouth is open. His expression remains consistent. Person A's mouth is open and her eyes are wide. Her expression remains consistent.
Tone of voice: Person B's voice is low and questioning. Person A's voice is higher and sounds like a response.
Where the speaker is looking: Person B is looking at Person A. Person A is looking at Person B.
Speaker body: Person B is standing upright. Person A has her arms crossed.
Other people: Person C (man, left of frame, dark suit) is standing with his back to the camera. Person D (woman, right background, dark top) is standing with her hands clasped.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in a room with a textured wall, where people are standing and talking.
```

**v7:**

```
The man in the dark suit is the main speaker. He says, "How do you know so much about this?"

The man's eyebrows move together and down. His forehead wrinkles. His eyes narrow slightly. His mouth opens and closes. His lips move to form words. His cheeks move with his mouth.

The man's torso is mostly still. His head moves slightly. His arms are not visible. His hands are not visible. His legs are not visible.

The speaker's voice is at a medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after the word "this."
```
</details>

### `video_177_0` · cue: face · emotions: surprise, engagement/attention · negated
**Fact:** His eyebrows are often raised.  
**Correct (B):** The raised eyebrows do not indicate surprise or interest.  
**Other (A):** The raised eyebrows indicate surprise or interest.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | The voice is high-pitched, loud, and fast. There is a rising inflection at the end of the sentence. | The speaker's voice is at a medium pitch. The pitch rises slightly at the end of the sentence. The voice is loud. The pace is moderate. There is a pause after the word "you." The word "Thank" is said with extra emphasis. |
| Decider's reasoning | The raised eyebrows, combined with the wide eyes and high-pitched, fast speech, suggest heightened emotional arousal. Given the context of a sudden or unexpected interaction in a hallway, the eyebrows likely signal surprise or interest rather than a neutral or dismissive stance. This aligns more with interpretation A. | The man's eyebrows are frequently raised, but this occurs in sync with his verbal expression of gratitude. Given that he says "Thank you" with emphasis on "Thank" and a rising pitch, the raised eyebrows likely serve to reinforce sincerity or warmth rather than signal surprise or interest. This suggests the gesture is more aligned with expressing appreciation than conveying curiosity or astonishment. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: Thank you.
Speaker face: At the start, the corners of her mouth are pulled up and her eyes are narrowed. By the end, her mouth is open and her eyes are wide.
Tone of voice: The voice is high-pitched, loud, and fast. There is a rising inflection at the end of the sentence.
Where the speaker is looking: She is looking at Person B.
Speaker body: Person A is standing still with her arms at her sides.
Other people: Person B is looking at Person A. His mouth is open and his eyes are wide.
Physical contact: Not applicable.
Other sounds: Not applicable.
Setting: The scene is indoors, in a hallway with a bulletin board and a light fixture on the wall.
```

**v7:**

```
The man is the main speaker. He says, "Thank you."

The man's eyebrows move up and down. His forehead wrinkles and smooths out. His eyes open and close slightly. His mouth opens and closes. His lips move in different directions. His cheeks move up and down.

The man's torso moves slightly. His right arm is bent at the elbow. His right hand holds a white object. His left arm is not visible.

The speaker's voice is at a medium pitch. The pitch rises slightly at the end of the sentence. The voice is loud. The pace is moderate. There is a pause after the word "you." The word "Thank" is said with extra emphasis.
```
</details>

### `video_206_2` · cue: face · emotions: intensity/emphasis · negated
**Fact:** Her mouth is open.  
**Correct (A):** Her mouth being open does not suggest that she is shouting or expressing strong displeasure.  
**Other (B):** Her mouth being open suggests she is shouting or expressing strong displeasure.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✗ | A ✓ |
| Voice as described | The pitch is high and the pace is fast. The voice is strained and loud. | Her voice is high. It rises and falls. It is loud. It is fast. There are no pauses. She emphasizes the words "crown molding" and "dormer windows." |
| Decider's reasoning | The speaker's mouth is open in conjunction with other signs such as wide eyes, raised eyebrows, a high-pitched and loud voice, and a fast, strained delivery. These cues collectively suggest heightened emotional arousal, which is more consistent with shouting or expressing strong displeasure than with neutral or calm speech. The open mouth is likely part of an expressive, emotionally charged vocalization rather than a casual or conversational state. | The woman's mouth is open in the context of fast, loud, high-pitched speech with no pauses, and she emphasizes specific words with animated facial expressions. These cues suggest she is excited or enthusiastic rather than angry or displeased. Her overall body language, including hand and arm movements, supports energetic communication rather than aggression. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B
Speech: [inaudible]
Speaker face: At the start, her eyebrows are raised and her eyes are wide. By the end, her eyebrows are lowered and her eyes are narrowed. Her mouth is open at the start and closed by the end.
Tone of voice: The pitch is high and the pace is fast. The voice is strained and loud.
Where the speaker is looking: She looks at Person A throughout the clip.
Speaker body: Her hands are raised in front of her body with palms facing Person A. She lowers her hands and then raises them again.
Other people: Person A has his hands in his pockets. He looks at Person B.
Physical contact: Not applicable.
Other sounds: Not applicable.
Setting: The scene is indoors, in a furnished room with a couch, a refrigerator, and a door.
```

**v7:**

```
The main speaker is the woman. She says, "And the crown molding and the dormer windows in the attic."

Her eyebrows raise and lower. Her forehead wrinkles slightly. Her eyes open wider and then narrow. Her nose flares a little. Her cheeks move up and down. Her mouth opens and closes. Her lips press together and then part.

Her hands move up and down. Her arms move back and forth. Her torso shifts slightly. Her shoulders move up and down.

Her voice is high. It rises and falls. It is loud. It is fast. There are no pauses. She emphasizes the words "crown molding" and "dormer windows."
```
</details>

### `video_207_0` · cue: face · emotions: sadness · negated
**Fact:** Her facial expression is downcast.  
**Correct (B):** The downcast facial expression is not often associated with sadness or disappointment.  
**Other (A):** The downcast facial expression is often associated with sadness or disappointment.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | The pitch is mid-range and the pace is moderate. The voice is clear and steady. | The speaker's voice is at a medium pitch. It rises slightly on the word "favorite." The pace is moderate. There is a brief pause after "favorite." The word "thank" is spoken with a slight emphasis. |
| Decider's reasoning | The downcast facial expression, combined with narrowed eyes and drawn-together eyebrows, suggests a more complex emotional state than simple sadness. However, the context—receiving flowers and expressing gratitude—indicates a moment of emotional vulnerability rather than disappointment. This aligns more with interpretation A, as the expression may reflect a heartfelt or shy reaction to being appreciated. | The speaker's downcast facial expression, combined with her holding flowers and expressing gratitude, suggests a moment of emotional sincerity rather than sadness. Her voice rises slightly on "favorite" and she emphasizes "thank," indicating genuine appreciation, which aligns more with interpretation B. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: "Joey, they're my favorite. Thank you."
Speaker face: At the start, her eyebrows are slightly raised and her eyes are open. By the end, her eyebrows are drawn together and her eyes are narrowed. Her mouth is open at the start and closed by the end.
Tone of voice: The pitch is mid-range and the pace is moderate. The voice is clear and steady.
Where the speaker is looking: She looks at Person B, then looks down at the flowers she is holding.
Speaker body: She holds a bouquet of white lilies with both hands. She brings the bouquet closer to her chest.
Other people: Person B is visible from the back and side. He is standing still and looking at Person A.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in what appears to be an apartment kitchen or living area. A woman is receiving flowers from a man.
```

**v7:**

```
The main speaker is the woman in the black shirt. She says, "Joey, they're my favorite. Thank you."

The woman's eyebrows move slightly down and together. Her forehead shows small wrinkles. Her eyes look down at the flowers. Her mouth opens and closes as she speaks. Her lips move to form the words.

The woman holds the flowers with both hands. Her arms are bent at the elbows. Her torso is upright. Her hands move slightly as she holds the flowers.

The speaker's voice is at a medium pitch. It rises slightly on the word "favorite." The pace is moderate. There is a brief pause after "favorite." The word "thank" is spoken with a slight emphasis.
```
</details>

### `video_208_0` · cue: face · emotions: anger · negated
**Fact:** Her facial expressions include furrowed brows and a stern look.  
**Correct (B):** Her facial expressions do not align with the emotion of anger.  
**Other (A):** Her facial expressions align with the emotion of anger.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | The pitch is mid-range and steady. The pace is moderate. The voice is clear and the volume is consistent. | The speaker's voice is at a moderate pitch. It rises slightly at the end of the phrase. The pace is moderate. There is a slight pause after the word "No." The word "Phoebe" is spoken with a slightly higher pitch. |
| Decider's reasoning | The furrowed brows and stern look, combined with narrowed eyes and a creased forehead, are strong indicators of anger or frustration. These facial cues, especially when paired with a shift from an open, wide-eyed expression to a more closed, intense one, suggest a rising emotional intensity consistent with anger. The gesture of moving hands outward with palms up may also signal exasperation or a defensive stance, reinforcing the interpretation of anger. | The furrowed brows and stern look could suggest frustration or emphasis, but the overall context—moderate pitch, slight pause, and controlled gestures—does not indicate strong anger. The speaker's tone and body language seem more focused on clarifying a point than expressing hostility. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A's mouth moves while the words are heard.
Speech: Person A: "No, I live with Phoebe."
Speaker face: At the start, her eyebrows are slightly raised, her forehead is smooth, her eyes are wide, and her mouth is open. By the end, her eyebrows are lowered, her forehead is creased, her eyes are narrowed, and her mouth is closed.
Tone of voice: The pitch is mid-range and steady. The pace is moderate. The voice is clear and the volume is consistent.
Where the speaker is looking: Person A looks at Person B throughout the clip.
Speaker body: Person A's hands are clasped in front of her. She then unclasps them and gestures with both hands, palms up, moving them outwards and then inwards.
Other people: Person B (man, right of frame, blue sweater) stands still, looking at Person A. His mouth is closed and his expression is neutral.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene takes place in a hallway with a dark green door and beige walls. A woman and a man are standing and talking.
```

**v7:**

```
The woman in the red top is the main speaker. She says, "No, I live with Phoebe."

The woman's eyebrows move slightly upwards and then lower. Her forehead shows some creases. Her eyes remain open and focused. Her mouth opens and closes as she speaks. Her lips move to form words. Her cheeks move with the opening and closing of her mouth.

The woman's hands are clasped together in front of her. She then moves her hands apart and gestures with them. Her arms move slightly as she gestures. Her torso remains mostly still.

The speaker's voice is at a moderate pitch. It rises slightly at the end of the phrase. The pace is moderate. There is a slight pause after the word "No." The word "Phoebe" is spoken with a slightly higher pitch.
```
</details>

### `video_213_0` · cue: gaze · emotions: anger, intensity/emphasis · negated
**Fact:** The intensity of her gaze.  
**Correct (A):** The intensity of her gaze does not indicate that she is expressing strong emotions, likely frustration or annoyance.  
**Other (B):** The intensity of her gaze indicates that she is expressing strong emotions, likely frustration or annoyance.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✗ | A ✓ |
| Voice as described | The pitch is mid-range and steady. The pace is moderate. The voice is clear and the words are articulated distinctly. | Her voice is at a moderate pitch, with a slight rise at the end of the phrase. The pace is steady and conversational, with a brief pause after the first sentence. |
| Decider's reasoning | The narrowing of Person B’s eyes and lowering of her eyebrows by the end of the clip suggest a shift toward a more intense or confrontational expression. This, combined with her steady, clear voice and direct gaze at Person C, points to controlled emotional intensity rather than a lack of emotion. Therefore, the intensity of her gaze likely reflects suppressed frustration or annoyance. | The woman's facial expressions, such as raised eyebrows, forehead wrinkles, and minimal nose flaring, suggest some level of emotional engagement or tension. However, her steady pace, moderate pitch, and mostly still torso indicate a controlled demeanor rather than overt frustration. The intensity of her gaze may reflect focus or emphasis rather than strong negative emotions. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B
Speech: You'll have a last kiss.
Speaker face: At the start, her eyebrows are slightly raised and her eyes are open. By the end, her eyebrows are lowered and her eyes are narrowed. Her mouth is open at the start and closed by the end.
Tone of voice: The pitch is mid-range and steady. The pace is moderate. The voice is clear and the words are articulated distinctly.
Where the speaker is looking: She is looking at Person C.
Speaker body: Her body is upright and she is standing still.
Other people: Person A is standing to the left, facing away from the camera. Person C is standing to the right, facing Person B.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is in a kitchen with stainless steel appliances and a brick wall.
```

**v7:**

```
The woman in the blue jacket is the main speaker. Her mouth opens and closes as she speaks, her lips move to form words, and her jaw shifts slightly with the rhythm of her speech.

Her eyebrows raise and lower, her forehead wrinkles slightly, her eyes blink and shift focus, her nose flares minimally, her cheeks move with her mouth, and her lips purse and stretch as she talks.

Her torso remains mostly still, facing the person she is speaking to. Her arms are down at her sides, and her hands are not visible in the frame.

Her voice is at a moderate pitch, with a slight rise at the end of the phrase. The pace is steady and conversational, with a brief pause after the first sentence.
```
</details>

### `video_215_0` · cue: face · emotions: other
**Fact:** Her mouth is slightly open.  
**Correct (B):** Her mouth being slightly open suggests that she is in the middle of speaking.  
**Other (A):** Her mouth being slightly open does not suggest that she is in the middle of speaking.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | The pitch is high. The speed is moderate. The voice is clear. | The speaker's voice is at a medium pitch. It rises slightly at the end of the first sentence. The pace is moderate. There is a short pause between the two sentences. |
| Decider's reasoning | The observation states that Person B's mouth is slightly open, and this occurs while Person A is speaking. However, Person B's mouth is also described as closed at another point, and there is no indication that Person B is vocalizing. Since the mouth being slightly open could be due to surprise or listening rather than speaking, and no speech is heard from Person B, it is more likely that the open mouth reflects a reaction rather than active speech. | The woman's mouth is slightly open while she is actively speaking, as evidenced by her lips moving to form words and her cheeks moving in coordination with speech. This indicates that the open mouth is directly related to her articulation, making it a sign that she is in the middle of speaking. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B's mouth moves while the words are heard. Person A is speaking.
Speech: Person A: "What are you talking about? These aren't mine."
Speaker face: Person B's eyebrows are raised. Her eyes are open and looking at Person A. The corners of her mouth are pulled up. Her mouth is open. Her eyebrows are lowered. Her eyes are narrowed. Her mouth is closed.
Tone of voice: The pitch is high. The speed is moderate. The voice is clear.
Where the speaker is looking: Person B is looking at Person A.
Speaker body: Person B's right hand is holding a black object. Her left hand is gesturing. Person A's back is to the camera.
Other people: Person A is facing Person B. Person A's back is to the camera.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in a room with furniture and a cardboard box.
```

**v7:**

```
The woman is the main speaker. She says, "What are you talking about? These aren't mine."

The woman's eyebrows move slightly up and down. Her forehead shows small wrinkles. Her eyes look forward and blink. Her nose remains still. Her cheeks move as she speaks. Her mouth opens and closes, and her lips move to form words.

The woman's left hand holds an object. Her right hand moves from her side to her chest and back down. Her torso remains mostly still. Her shoulders move slightly with her breathing.

The speaker's voice is at a medium pitch. It rises slightly at the end of the first sentence. The pace is moderate. There is a short pause between the two sentences.
```
</details>

### `video_298_0` · cue: gaze · emotions: joy, engagement/attention
**Fact:** Her eyes are focused on the book.  
**Correct (B):** Her eyes being focused on the book indicates her engagement with the content.  
**Other (A):** Her eyes being focused on the book suggests she is using it as a distraction from her sadness.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | The pitch is mid-range and the speed is moderate. The voice is clear and steady. | Her voice is at a medium pitch. It rises slightly at the end. The pace is moderate. There is a slight pause after "her." |
| Decider's reasoning | The observation that Person A's eyes are focused on the book could suggest engagement, especially since she is holding it open and speaking directly to Person B. However, the narrowing of her eyes and lowered eyebrows by the end of the clip indicate emotional tension or concern, which might imply she is using the book as a distraction. Given the context of asking a personal question ("Did you break up with her?"), the emotional cues lean toward interpretation A. | The woman's facial expressions—raised and inward-moving eyebrows, forehead wrinkles, and narrowed eyes—suggest emotional tension or concern, possibly related to the sensitive topic of a breakup. However, her eyes are fixed on the book, and her hands are gently moving over it, indicating she may be using it as a grounding or emotional buffer. While interpretation A suggests sadness, the lack of overt signs of distress (like tears or a shaky voice) makes B more plausible, as her focus could reflect genuine engagement rather than avoidance. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: Did you break up with her?
Speaker face: At the start, her eyebrows are slightly raised and her eyes are narrowed. By the end, her eyebrows are lowered and her eyes are narrowed.
Tone of voice: The pitch is mid-range and the speed is moderate. The voice is clear and steady.
Where the speaker is looking: She looks at Person B while speaking.
Speaker body: She holds a book open with both hands and keeps her arms relatively still.
Other people: Person B looks at Person A, then looks down at the book, then looks back at Person A. His head is tilted slightly.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in a living room, where two people are sitting on a couch and looking at a book.
```

**v7:**

```
The main speaker is the woman. She says, "Did you break up with her?"

Her eyebrows move slightly upward and inward. Her forehead shows small wrinkles. Her eyes narrow a little. Her mouth opens and closes with the words. Her lips move to form the sounds. Her cheeks rise slightly.

Her arms are bent with hands holding a book. Her legs are together. Her torso is upright. Her hands move slightly on the book.

Her voice is at a medium pitch. It rises slightly at the end. The pace is moderate. There is a slight pause after "her."
```
</details>

### `video_298_2` · cue: hands/gesture · emotions: joy, engagement/attention
**Fact:** The woman is holding a book and appears to be reading it.  
**Correct (A):** Her body language suggests that she is engaged and focused on the content of the book.  
**Other (B):** Her body language does not suggest that she is engaged and focused on the content of the book.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✗ | A ✓ |
| Voice as described | The pitch is mid-range and the speed is moderate. The voice is clear and steady. | Her voice is at a medium pitch. It rises slightly at the end. The pace is moderate. There is a slight pause after "her." |
| Decider's reasoning | The woman is holding the book open with both hands and maintaining eye contact with Person B while speaking, which indicates she is actively involved in the conversation rather than focusing on reading. Her steady voice and moderate speech pace further suggest she is engaged in dialogue, not absorbed in the book. Therefore, her body language does not support the idea that she is focused on the book's content. | The woman’s facial expressions—raised and inward-moving eyebrows, forehead wrinkles, and narrowed eyes—indicate surprise or skepticism, which aligns more with reacting to something she just read rather than being passively engaged in reading. Additionally, her voice rising at the end of the sentence and the slight pause after “her” suggest she is processing and reacting to the content, not simply reading mindlessly. These cues point to active cognitive engagement with the material. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: Did you break up with her?
Speaker face: At the start, her eyebrows are slightly raised and her eyes are narrowed. By the end, her eyebrows are lowered and her eyes are narrowed.
Tone of voice: The pitch is mid-range and the speed is moderate. The voice is clear and steady.
Where the speaker is looking: She looks at Person B while speaking.
Speaker body: She holds a book open with both hands and keeps her arms relatively still.
Other people: Person B looks at Person A, then looks down at the book, then looks back at Person A. His head is tilted slightly.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in a living room, where two people are sitting on a couch and looking at a book.
```

**v7:**

```
The main speaker is the woman. She says, "Did you break up with her?"

Her eyebrows move slightly upward and inward. Her forehead shows small wrinkles. Her eyes narrow a little. Her mouth opens and closes with the words. Her lips move to form the sounds. Her cheeks rise slightly.

Her arms are bent with hands holding a book. Her legs are together. Her torso is upright. Her hands move slightly on the book.

Her voice is at a medium pitch. It rises slightly at the end. The pace is moderate. There is a slight pause after "her."
```
</details>

### `video_319_3` · cue: posture/movement · emotions: fear/anxiety
**Fact:** The man's posture is slightly hunched.  
**Correct (B):** The hunched posture indicates a sense of tension or unease.  
**Other (A):** The hunched posture does not indicate a sense of tension or unease.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | The pitch is mid-range and the pace is moderate. The voice is clear and steady. | The speaker's voice is of a medium pitch. It is steady in loudness and has a moderate speed. There are no noticeable pauses or changes in emphasis. |
| Decider's reasoning | The man's hunched posture, combined with his body being angled toward Person A and his direct gaze, suggests he is engaged in the conversation. While a hunched posture can sometimes signal tension, in this context it may simply reflect a relaxed or thoughtful stance rather than unease. Given the lack of other signs of discomfort, such as fidgeting or avoiding eye contact, interpretation A seems more plausible. | The hunched posture, combined with the slight eyebrow movements and forehead creases, suggests the man may be experiencing some internal tension or discomfort. While his voice remains steady and his torso mostly still, the subtle facial cues and posture could indicate unease rather than a relaxed state. Therefore, the hunched posture is more likely signaling tension or unease. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A (woman, left of frame, red sweater)
Speech: Richard used to do it, didn't he?
Speaker face: At the start, her eyes are narrowed and her mouth is closed. By the end, her mouth is slightly open and her eyes are looking forward.
Tone of voice: The pitch is mid-range and the pace is moderate. The voice is clear and steady.
Where the speaker is looking: She is looking at Person B.
Speaker body: Her arms are crossed in front of her body.
Other people: Person B (man, right of frame, dark suit) is standing with his body angled toward Person A. He is looking at Person A.
Physical contact: There is no physical contact.
Other sounds: Not audible.
Setting: The scene is indoors, in a room with a large pillar, where people are standing and talking.
```

**v7:**

```
The man in the dark suit and patterned tie is the main speaker. He says, "Richard used to do it, didn't he?"

The man's eyebrows move slightly up and down. His forehead shows some creases. His eyes look towards the woman. His nose remains still. His cheeks move as he speaks. His mouth opens and closes, and his lips move to form words.

The man's torso is mostly still. His head turns slightly towards the woman. His arms are down by his sides. His hands are not visible.

The speaker's voice is of a medium pitch. It is steady in loudness and has a moderate speed. There are no noticeable pauses or changes in emphasis.
```
</details>

### `video_319_4` · cue: hands/gesture · emotions: anger
**Fact:** The man is making strong points.  
**Correct (B):** He is possibly expressing frustration or annoyance.  
**Other (A):** He is confidently sharing his ideas and feels pleased with the discussion.  
*Baseline (Neha) was wrong.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | The pitch is mid-range and the pace is moderate. The voice is clear and steady. | The speaker's voice is of a medium pitch. It is steady in loudness and has a moderate speed. There are no noticeable pauses or changes in emphasis. |
| Decider's reasoning | The man is making strong points, which suggests he is actively engaged and assertive in the conversation. His body language—facing Person A directly and maintaining eye contact—indicates confidence and focus rather than frustration. Since there are no signs of tension or negative cues in his posture or expression, the interpretation that he is confidently sharing ideas fits better with the observed behavior. | The man's eyebrows moving slightly up and down and the creases on his forehead suggest mild tension or concentration rather than relaxation or pleasure. His steady voice and lack of emphasis or pauses indicate he is making a point deliberately, but without emotional escalation. The combination of focused facial cues and controlled delivery leans more toward frustration or annoyance than confidence and pleasure. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A (woman, left of frame, red sweater)
Speech: Richard used to do it, didn't he?
Speaker face: At the start, her eyes are narrowed and her mouth is closed. By the end, her mouth is slightly open and her eyes are looking forward.
Tone of voice: The pitch is mid-range and the pace is moderate. The voice is clear and steady.
Where the speaker is looking: She is looking at Person B.
Speaker body: Her arms are crossed in front of her body.
Other people: Person B (man, right of frame, dark suit) is standing with his body angled toward Person A. He is looking at Person A.
Physical contact: There is no physical contact.
Other sounds: Not audible.
Setting: The scene is indoors, in a room with a large pillar, where people are standing and talking.
```

**v7:**

```
The man in the dark suit and patterned tie is the main speaker. He says, "Richard used to do it, didn't he?"

The man's eyebrows move slightly up and down. His forehead shows some creases. His eyes look towards the woman. His nose remains still. His cheeks move as he speaks. His mouth opens and closes, and his lips move to form words.

The man's torso is mostly still. His head turns slightly towards the woman. His arms are down by his sides. His hands are not visible.

The speaker's voice is of a medium pitch. It is steady in loudness and has a moderate speed. There are no noticeable pauses or changes in emphasis.
```
</details>

### `video_334_1` · cue: face · emotions: fear/anxiety
**Fact:** The man has wide eyes and a slightly open mouth.  
**Correct (B):** His facial expressions suggest a combination of fear and anxiety.  
**Other (A):** His facial expressions suggest a combination of surprise and anger.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | Person B's voice is low, loudness is moderate, speed is moderate, voice quality is tense. Person A's voice is low, loudness is moderate, speed is moderate, voice quality is tense. | The speaker's voice is at a medium pitch. It rises slightly at the end of the first sentence. The pace is moderate. There is a pause between the two sentences. The word "fit" is said with a slight emphasis. |
| Decider's reasoning | The man's wide eyes and slightly open mouth are commonly associated with surprise, but the context of tense voice, narrowed eyes, and lowered eyebrows suggests underlying anger rather than fear. While fear can involve wide eyes, it is typically paired with other cues like flinching or avoidance, which are absent here. The combination of surprise and anger fits the overall tense and confrontational tone of the interaction. | The wide eyes and slightly open mouth, combined with the downward eyebrow movement and forehead wrinkles, are more consistent with expressions of fear or anxiety rather than anger. Anger typically involves more intense facial tension and a fixed stare, whereas the speaker's gaze shifting and subtle body movements suggest unease or nervousness. The emphasis on "fit" and the hesitant tone further support anxiety about social acceptance rather than anger. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person B's mouth moves while the words are heard. Person A's mouth moves while the words are heard.
Speech: Person B: "Well, nothing yet. They really hate you and I want to fit in." Person A: "..."
Speaker face: Person B's eyebrows are lowered, forehead is creased, eyes are narrowed, mouth is open with corners down. Person A's eyebrows are lowered, forehead is creased, eyes are narrowed, mouth is open with corners down.
Tone of voice: Person B's voice is low, loudness is moderate, speed is moderate, voice quality is tense. Person A's voice is low, loudness is moderate, speed is moderate, voice quality is tense.
Where the speaker is looking: Person B is looking at Person A. Person A is looking at Person B.
Speaker body: Person B's arms are at his sides. Person A's arms are at her sides.
Other people: Person A's face is visible. Person A is looking at Person B. Person A's posture is upright.
Physical contact: Not applicable.
Other sounds: Not applicable.
Setting: The scene is in a kitchen with a brick wall in the background.
```

**v7:**

```
The main speaker is the man in the white shirt and red tie. He says, "Well, nothing yet. They really hate you and I want to fit in."

The man's eyebrows move down and together. His forehead wrinkles. His eyes look down and then up. His mouth opens and closes. His lips move to form words. His cheeks move slightly.

The man's hands move up and down. His arms move back and forth. His torso shifts slightly. His shoulders move up and down.

The speaker's voice is at a medium pitch. It rises slightly at the end of the first sentence. The pace is moderate. There is a pause between the two sentences. The word "fit" is said with a slight emphasis.
```
</details>

### `video_368_2` · cue: face · emotions: anger, sadness · negated
**Fact:** There is a slight furrow in her brow and she occasionally looks downwards.  
**Correct (B):** These do not suggest that she might also be feeling a bit of annoyance or disappointment.  
**Other (A):** These suggest that she might also be feeling a bit of annoyance or disappointment.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | High-pitched, loud, fast, with a strained quality. | The speaker's voice is high-pitched. It rises in pitch. It is loud. It is spoken quickly. There are no pauses. The words "Oh my god" are said with extra emphasis. |
| Decider's reasoning | The slight furrow in her brow and downward glances could indicate internal conflict or negative emotion, especially when combined with her strained, high-pitched tone and wide eyes—signs of distress or frustration. While her initial raised arms and open mouth suggest surprise or alarm, the brow furrow and downward gaze may signal a shift toward annoyance or disappointment beneath the surface. These subtle cues align more with interpretation A, as they suggest a complex emotional state that includes frustration rather than being absent of it. | The slight furrow in her brow and downward glances could indicate a mix of emotions, but given the overall context of surprise and heightened emotion—evidenced by wide eyes, raised arms, and a high-pitched, emphatic delivery—the furrow is more likely a sign of intense surprise or concern rather than annoyance or disappointment. The lack of negative vocal cues and the physical expressiveness point more toward a strong emotional reaction than irritation. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: Oh my god.
Speaker face: At the start, the corners of her mouth are pulled up and her eyes are narrowed. At the end, her mouth is open and her eyes are wide.
Tone of voice: High-pitched, loud, fast, with a strained quality.
Where the speaker is looking: Looking up and to the right.
Speaker body: Arms raised with hands open, then both hands move to her head.
Other people: not visible
Physical contact: not visible
Other sounds: not audible
Setting: The scene is in a kitchen with shelves of jars and pots in the background.
```

**v7:**

```
The main speaker is the woman in the black dress. She says, "Oh my god."

The woman's eyebrows move upward and inward. Her forehead wrinkles. Her eyes widen. Her mouth opens and her lips move. Her cheeks rise.

Her arms are raised. Her hands move up and down. Her hands move to her head. Her hands move away from her head.

The speaker's voice is high-pitched. It rises in pitch. It is loud. It is spoken quickly. There are no pauses. The words "Oh my god" are said with extra emphasis.
```
</details>

### `video_379_0` · cue: voice/speech · emotions: engagement/attention
**Fact:** The speaker's body language is open and inviting, with a slight lean forward.  
**Correct (A):** The open and inviting body language with a slight lean forward indicates engagement and interest in the conversation.  
**Other (B):** The open and inviting body language with a slight lean forward does not indicate engagement and interest in the conversation.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✗ | A ✓ |
| Voice as described | The pitch is low and the pace is slow. The voice is steady and the words are spoken clearly. | The speaker's voice is of medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after the word "out." |
| Decider's reasoning | The speaker is looking down at the chick throughout the clip, which suggests his focus is on the animal rather than on Person B. Although the body language is described as open and inviting, the lack of eye contact with Person B and the consistent focus on the chick imply that the speaker's attention is directed toward the animal, not the interaction. Therefore, the body language may not reflect engagement in the conversation. | The speaker's open posture, slight forward lean, and gentle hand movements while holding a small bird suggest a sense of care and connection. Combined with the relieved tone and moderate pace, this body language aligns more with genuine engagement and interest in the moment. Therefore, interpretation A is more consistent with the observed cues. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: Well, at least we got these little guys out.
Speaker face: At the start, Person A's eyebrows are slightly raised and his forehead is smooth. His eyes are open and looking down. By the end, his eyebrows are lowered and his forehead is creased. His eyes are narrowed and his mouth is open.
Tone of voice: The pitch is low and the pace is slow. The voice is steady and the words are spoken clearly.
Where the speaker is looking: Person A is looking down at the chick in his hands for the entire duration of the clip.
Speaker body: Person A is sitting on the floor with his legs bent. He holds a small white chick in his cupped hands. His hands move slightly as he speaks.
Other people: Person B is sitting on the floor to the right of Person A. He is holding a small yellow duckling. His head is turned towards Person A and he is looking at the duckling in his hands.
Physical contact: Person A is holding a chick in his hands. Person B is holding a duckling in his hands.
Other sounds: Not audible.
Setting: The scene takes place indoors on a carpeted floor. Two men are sitting on the floor holding small birds.
```

**v7:**

```
The main speaker is the man in the light blue striped shirt. He says, "Well, at least we got these little guys out."

The man in the striped shirt's eyebrows move down and together. His forehead shows wrinkles. His eyes close and then open. His mouth opens and closes. His lips move to form words. His cheeks move slightly.

The man in the striped shirt holds a small white bird in his hands. His arms are bent at the elbows. His hands move slightly as he speaks. His torso is upright. His legs are not visible.

The speaker's voice is of medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after the word "out."
```
</details>

### `video_383_1` · cue: face · emotions: intensity/emphasis
**Fact:** Her facial expression appears to be neutral to slightly concerned.  
**Correct (A):** The emotion of the speaker can be identified as a combination of concern and seriousness.  
**Other (B):** The speaker is surprised by the situation, which is reflected in her neutral to slightly concerned facial expression.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | B ✗ | A ✓ |
| Voice as described | The pitch is mid-range and the pace is moderate. The voice is breathy and the words are spoken with a slight upward inflection at the end. | Her voice is at a medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after "No." The word "fun" is spoken with a slightly higher pitch. |
| Decider's reasoning | The speaker's initial wide eyes and raised eyebrows suggest surprise, but these features transition to narrowed eyes and lowered brows, indicating a shift toward concern or seriousness. While her expression is described as neutral to slightly concerned, the initial signs of surprise are more consistent with the observation of her facial changes over time. Therefore, interpretation B aligns better with the observed progression of her expression. | The speaker's facial expression is described as neutral to slightly concerned, and her eyebrows move subtly while her forehead shows small wrinkles—both of which can indicate mild concern or thoughtfulness rather than surprise. Additionally, her voice rises slightly at the end of the sentence, suggesting uncertainty or hesitation, which aligns more with concern than surprise. The slight pause after "No" also indicates she is considering her words, reinforcing a thoughtful or serious tone rather than one of surprise. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A
Speech: I just thought it would be fun.
Speaker face: At the start, her eyebrows are slightly raised and her eyes are wide. By the end, her eyebrows are lowered and her eyes are narrowed. Her mouth is slightly open at the start and closes by the end.
Tone of voice: The pitch is mid-range and the pace is moderate. The voice is breathy and the words are spoken with a slight upward inflection at the end.
Where the speaker is looking: She is looking at Person B.
Speaker body: She is standing with her arms at her sides and her body facing Person B.
Other people: Person B is standing to the right of the frame, facing Person A. His face is partially visible. He is wearing a blue shirt with a pattern on it.
Physical contact: Not visible.
Other sounds: Not audible.
Setting: The scene is indoors, in a room with framed pictures on the wall and a mirror. Person A and Person B are standing and talking to each other.
```

**v7:**

```
The main speaker is the woman in the red dress. She says, "No, I just thought it would be fun."

Her eyebrows move slightly up and down. Her forehead shows small wrinkles. Her eyes look forward and then shift to the side. Her mouth opens and closes, and her lips move with the words.

Her arms are at her sides. Her hands are not visible. Her torso is still. Her shoulders are level.

Her voice is at a medium pitch. It rises slightly at the end of the sentence. The pace is moderate. There is a slight pause after "No." The word "fun" is spoken with a slightly higher pitch.
```
</details>

### `video_393_0` · cue: face · emotions: intensity/emphasis · negated
**Fact:** His mouth is open.  
**Correct (B):** The open mouth does not indicate that he is speaking with conviction and determination.  
**Other (A):** The open mouth indicates that he is speaking with conviction and determination.  
*Baseline (Neha) was right.*

| | v3 | v7 |
| --- | --- | --- |
| Answer | A ✗ | B ✓ |
| Voice as described | Person A's voice is loud and strained. Person B's voice is lower and calmer. | The speaker's voice is low and steady. The pace is moderate. There are slight pauses between phrases. The words "one girl" are spoken with a slightly lower pitch. |
| Decider's reasoning | The observation that Person A's mouth is open while he is speaking, combined with his loud and strained voice, suggests that he is emphasizing his words with intensity. This aligns more closely with speaking with conviction and determination rather than simply being in the act of speaking. Therefore, Interpretation A is more consistent with the observed body language and vocal tone. | The man's mouth is open as part of normal speech, and his voice is low, steady, and measured with slight pauses, suggesting a calm and deliberate delivery rather than strong conviction or determination. His facial expressions, including raised eyebrows and forehead wrinkles, may indicate thoughtfulness or mild concern, not assertiveness. Therefore, the open mouth is simply a functional part of speaking, not a sign of strong conviction. |

<details><summary>Full descriptions</summary>

**v3:**

```
Speaker: Person A's mouth moves while the words are heard. Person B's mouth moves while the words are heard. Person A is speaking.
Speech: Person A: "Well, that's all right, sir, and that's just one girl."
Person B: [inaudible]
Speaker face: Person A's mouth is open. Person B's mouth is closed. Person B's mouth opens.
Tone of voice: Person A's voice is loud and strained. Person B's voice is lower and calmer.
Where the speaker is looking: Person A looks at Person B. Person B looks at Person A.
Speaker body: Person A holds a glass with a straw in his left hand. Person B raises his right hand and points his index finger.
Other people: Person A holds a glass with a straw in his left hand. Person B raises his right hand and points his index finger.
Physical contact: Person B raises his right hand and points his index finger.
Other sounds: Not audible.
Setting: The scene is indoors, in a dimly lit bar or club, with people sitting at tables.
```

**v7:**

```
The man on the left is the main speaker. He says, "Well, that's all right, sir, and that's just one girl."

The man on the left's mouth opens wide and moves as he speaks. His eyebrows raise and lower. His forehead wrinkles. His eyes look forward and then shift to the right. His cheeks move with his mouth. His lips stretch and relax.

The man on the left holds a glass in his right hand. His left hand rests on the table. His torso remains mostly still. His head turns slightly to the right.

The speaker's voice is low and steady. The pace is moderate. There are slight pauses between phrases. The words "one girl" are spoken with a slightly lower pitch.
```
</details>
