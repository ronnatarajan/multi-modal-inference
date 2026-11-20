"""Tag VIBE questions using only the dataset's own text.

cue      : what kind of visual cue the `fact` describes (first matching rule wins)
emotions : the emotion / social meaning named in the CORRECT inference (every matching rule is kept)
negated  : the correct inference is phrased as a negation ("does not suggest anger")
"""
import json, re, collections, sys

CUES = [
    ("gaze", r"\b(gaz\w*|stare|staring|glanc\w*|eye contact|look(s|ing|ed)?( \w+)? (at|away|down|up|around|toward\w*|directly|into|off|to the side)|eyes (are )?(look\w*|direct\w*|fixed|focus\w*))\b"),
    ("smile/laugh", r"\b(smil\w*|grin\w*|laugh\w*|chuckl\w*|giggl\w*|smirk\w*)\b"),
    ("face", r"\b(face|facial|frown\w*|eyebrow\w*|brow\w*|forehead|eyes?|mouth|lips?|jaw\w*|cheeks?|nose|squint\w*|blink\w*|teeth|grimac\w*|expression\w*|tense|upset)\b"),
    ("voice/speech", r"\b(voice|tone|speak\w*|speech|says?|said|talk\w*|shout\w*|yell\w*|whisper\w*|sigh\w*|cry\w*|scream\w*|exclaim\w*|loud\w*|pitch)\b"),
    ("hands/gesture", r"\b(hands?|gestur\w*|finger\w*|point\w*|arms?|wav\w*|clap\w*|fist\w*|palms?|shrug\w*|hold\w*|touch\w*|grab\w*|hug\w*|wrist)\b"),
    ("posture/movement", r"\b(posture|lean\w*|stand\w*|sit\w*|walk\w*|mov\w*|head|nod\w*|shak\w*|tilt\w*|shoulders?|body|torso|turn\w*|step\w*|bend\w*|slump\w*|back|run\w*|jump\w*|position|lying|lies)\b"),
]

EMOTIONS = [
    ("anger", r"\b(ang(er|ry|rily)|frustrat\w*|annoy\w*|irritat\w*|furious|rage|mad|agitat\w*|exasperat\w*|hostil\w*|aggress\w*|confrontat\w*|defensive|indignan\w*)\b"),
    ("disgust/contempt", r"\b(disgust\w*|distaste|contempt\w*|disdain\w*|repuls\w*|revuls\w*|sarcas\w*|mock\w*|scorn\w*|dismissive|disapprov\w*)\b"),
    ("sadness", r"\b(sad\w*|upset\w*|sorrow\w*|grief|griev\w*|unhapp\w*|depress\w*|disappoint\w*|hurt|despair|distress\w*|regret\w*|melanchol\w*|dejected|heartbr\w*|cry\w*|tears?)\b"),
    ("fear/anxiety", r"\b(fear\w*|afraid|scared|anxi\w*|nervous\w*|worr\w*|tense|tension|panic\w*|alarm\w*|apprehens\w*|uneas\w*|discomfort|insecur\w*|stress\w*)\b"),
    ("surprise", r"\b(surpris\w*|shock\w*|astonish\w*|amaze\w*|disbelief|startl\w*|stunn\w*|incredul\w*|unexpected\w*)\b"),
    ("joy", r"\b(joy\w*|happ(y|iness|ily)|delight\w*|amus\w*|excit\w*|cheer\w*|pleas\w*|content(ed|ment)?|enthusias\w*|playful\w*|glee\w*|warm\w*|affection\w*|friendl\w*|positive|light-?hearted|humor\w*|elat\w*|relie\w*|thrill\w*|fond\w*|lov\w*)\b"),
    ("intensity/emphasis", r"\b(confiden\w*|assert\w*|emphatic\w*|emphas\w*|passion\w*|determin\w*|conviction|serious\w*|insist\w*|persua\w*|intens\w*|urgen\w*|earnest\w*|important|strong\w*|forceful\w*|animated)\b"),
    ("engagement/attention", r"\b(engag\w*|attenti\w*|focus\w*|listen\w*|participat\w*|involve\w*|interest\w*|absorb\w*|invested|concentrat\w*)\b"),
    ("calm/relaxed", r"\b(calm\w*|relax\w*|comfortabl\w*|at ease|composed|neutral|casual\w*|indifferen\w*|bored\w*|disinterest\w*|detach\w*)\b"),
    ("confusion/uncertainty", r"\b(confus\w*|uncertain\w*|unsure|hesita\w*|puzzl\w*|doubt\w*|perplex\w*|curio\w*|contemplat\w*|pensive|reflect\w*)\b"),
    ("embarrassment", r"\b(embarrass\w*|shy\w*|awkward\w*|bashful\w*|sheepish\w*|guilt\w*|asham\w*|self-conscious\w*)\b"),
]

NEG = re.compile(r"\b(not|n't|no|neither|nor)\b|n't\b", re.I)


def cue(fact):
    f = fact.lower()
    return next((name for name, pat in CUES if re.search(pat, f)), "other")


def emotions(text):
    t = text.lower()
    return [name for name, pat in EMOTIONS if re.search(pat, t)] or ["other"]


def tag(item):
    correct = item["inference_" + item["answer"]]
    return {"cue": cue(item["fact"]), "emotions": emotions(correct), "negated": bool(NEG.search(correct))}


if __name__ == "__main__":
    rows = [json.loads(l) for l in open(sys.argv[1])]
    for r in rows:
        r.update(tag(r))
    print("cue:", collections.Counter(r["cue"] for r in rows).most_common())
    print("emotion:", collections.Counter(e for r in rows for e in r["emotions"]).most_common())
    print("negated correct:", sum(r["negated"] for r in rows), "/", len(rows))
    for r in [r for r in rows if r["cue"] == "other"]:
        print("  cue=other:", r["fact"])
    oe = [r for r in rows if r["emotions"] == ["other"]]
    print("emotion=other:", len(oe))
    for r in oe[:20]:
        print("  ", r["inference_" + r["answer"]])
