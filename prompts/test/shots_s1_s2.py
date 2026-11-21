"""Hand-directed shots for Scenes 1 and 2 (test batch)."""

# who-tags: how Grok can tell people apart (by look AND clothes) in each scene
ID = {
 "1": {"chief": "the elderly man with snow-white hair and a full white beard, wearing the white kaftan",
       "grace": "the nurse in navy blue scrubs with her hair in cornrows pulled into a bun",
       "ronke": "the woman in the black dress with a white collar and a tight black head wrap",
       "segun": "the man with a grey-flecked beard in a charcoal suit, seen only on the phone screen"},
 "2": {"chief": "the elderly man with snow-white hair and a full white beard, lying in the hospital bed in a pale blue gown",
       "femi": "the man in the navy three-piece suit with rimless gold glasses and a short black beard",
       "gabriel": "the man in the grey suit and open white shirt with clear aviator glasses and a full beard",
       "hassan": "the doctor in the white coat over a light blue shirt, with greying hair and a salt-and-pepper beard",
       "lekan": "the heavy-set man in the black agbada with silver embroidery and gold-rimmed glasses",
       "ronke": "the woman in the black dress with a white collar and a tight black head wrap",
       "segun": "Segun (not on screen)"},
}

MOOD = {
 "1": "Dusk during a storm. Dim, moody, heavy with loneliness. Warm amber lamp light on the faces, cold blue-grey storm light from the window, deep soft shadows. Keep it exactly this dark; never brighten.",
 "2": "Night in a private hospital. Quiet, tense, grieving. Soft cool light from the room, a warm bedside lamp, rain on the window, deep soft shadows. Keep it exactly this dark; never brighten.",
}
SOUND = {"1": "rain on the windows, distant thunder, a clock ticking softly", "2": "a heart monitor beeping softly, rain on the glass, a quiet corridor hum"}

# Each shot: id, title, who, frame (the image), scene, focus, dialogue [(time, owner, line)], timeline [(time, action)], camera, start
# owner = a character key (speaks on screen) or "phone:<key>" (voice from the phone) or None
S = {"1": [], "2": []}
def shot(sc, **k): S[sc].append(k)

# ---------------- SCENE 1 ----------------
shot("1", id="1.1", title="The lagoon and the closed mansion", who=[],
 frame="High aerial view over the Lagos lagoon at dusk, dark storm clouds rolling in, a large white three-storey mansion on the water's edge with every curtain closed and one dim lit window.",
 scene="Opening of the film: a lonely white mansion on the Lagos lagoon at dusk as a storm arrives.",
 focus="The white mansion in the centre of the frame, its single dim window.",
 dialogue=[], timeline=[("0:00-0:03", "The camera glides over the dark grey water toward the mansion."), ("0:03-0:06", "Storm clouds roll overhead; the first rain begins to fall on the water."), ("0:06-0:08", "A soft flash of distant lightning far behind the house."), ("0:08-0:10", "The camera settles on the one dim lit window. Every curtain stays closed.")],
 camera="Slow, smooth drone glide forward and slightly down toward the mansion.", start="New image")

shot("1", id="1.2", title="Segun on the phone: 'Happy birthday, Daddy!'", who=["chief"],
 frame="Medium shot from the side of the dim bedroom: Chief stands at the rainy window in side profile, his face clearly visible and lit by the warm lamp, holding his phone up in front of him on a video call; the untouched birthday cake on a silver tray soft in the foreground.",
 scene="On his 75th birthday, a lonely old billionaire stands at his window taking a video call from his busy son.",
 focus="Chief's face in side profile on the right of the frame, the glowing phone in his hand.",
 dialogue=[("0:01-0:06", "phone:segun", "Happy birthday, Daddy! Did the wine arrive? I sent the expensive one.")],
 timeline=[("0:00-0:01", "Chief holds the phone up, still."), ("0:01-0:06", "Segun's cheerful voice plays from the phone. Chief listens, lips pressed together."), ("0:06-0:08", "Chief's jaw tightens; his eyes turn wet."), ("0:08-0:10", "He breathes out slowly through his nose, still silent.")],
 camera="Static camera, locked off.", start="New image")

shot("1", id="1.3", title="Chief: 'My son did not.'", who=["chief"],
 frame="Medium close-up of Chief at the rainy window, facing three-quarters toward the camera, the phone held up near his face, lamp light on one side of his face, cold window light on the other.",
 scene="The old man answers his son coldly on the video call.",
 focus="Chief's face, centre frame.",
 dialogue=[("0:01-0:03", "chief", "The wine arrived."), ("0:05-0:07", "chief", "My son did not.")],
 timeline=[("0:00-0:01", "Chief stares at the phone screen."), ("0:01-0:03", "He says the first line slowly."), ("0:03-0:05", "A heavy pause; he swallows, his eyes hard."), ("0:05-0:07", "He says the second line quietly, wounded."), ("0:07-0:10", "He holds the stare, jaw tight.")],
 camera="Very slow push-in toward his face.", start="New image")

shot("1", id="1.4", title="Segun laughs it off", who=["chief", "segun"],
 frame="Close-up over Chief's shoulder onto the phone screen in his hand: Segun in a busy glass office in Abuja, adjusting his tie and laughing; Chief's white beard and cheek soft in the foreground.",
 scene="The son laughs off his father's hurt on the video call.",
 focus="The phone screen in the centre, Segun's small face laughing.",
 dialogue=[("0:01-0:04", "phone:segun", "Daddy, please, not today.")],
 timeline=[("0:00-0:01", "Segun adjusts his tie on the screen."), ("0:01-0:04", "Segun's voice plays from the phone, laughing it off."), ("0:04-0:10", "Chief's cheek and beard in the foreground stay still; his hand grips the phone tighter.")],
 camera="Static close-up on the phone.", start="New image")

shot("1", id="1.5", title="Chief: the twins", who=["chief"],
 frame="Close-up of Chief's face, side-lit by the lamp, the phone held low in his hand, eyes wet but hard, rain streaks on the window behind him.",
 scene="The grandfather asks about the grandchildren he never sees.",
 focus="Chief's eyes and mouth, centre frame.",
 dialogue=[("0:01-0:08", "chief", "When are you bringing the twins? I last saw them when they were seven. They're twelve now.")],
 timeline=[("0:00-0:01", "Chief looks down at the phone."), ("0:01-0:08", "He speaks quietly and hurt, his voice cracking on 'twelve now'."), ("0:08-0:10", "He blinks slowly, holding back tears.")],
 camera="Static close-up.", start="New image")

shot("1", id="1.6", title="Chief: 'Strangers in a newspaper'", who=["chief"],
 frame="Same close-up of Chief's face by the rainy window, lamp light on his cheek, phone low in his hand.",
 scene="He tells his son the grandchildren are strangers to him.",
 focus="Chief's face, centre frame.",
 dialogue=[("0:01-0:06", "chief", "I know them from photographs, Segun. Like strangers in a newspaper.")],
 timeline=[("0:00-0:01", "Chief takes a breath."), ("0:01-0:06", "He speaks slowly and bitterly."), ("0:06-0:10", "He presses his lips together and looks away from the screen for a moment.")],
 camera="Very slow push-in.", start="Last frame of 1.5")

shot("1", id="1.7", title="Segun: 'It's a bad month'", who=["chief", "segun"],
 frame="Close-up over Chief's shoulder onto the phone screen: Segun in his office, distracted, glancing off to the side; Chief's white beard soft in the foreground.",
 scene="The son makes excuses on the video call.",
 focus="The phone screen, Segun's face.",
 dialogue=[("0:01-0:05", "phone:segun", "It's a bad month. The merger, the Senate committee…")],
 timeline=[("0:00-0:01", "Segun glances away on the screen."), ("0:01-0:05", "Segun's voice plays from the phone, rushed."), ("0:05-0:10", "Chief's beard in the foreground does not move; silence, rain.")],
 camera="Static close-up on the phone.", start="New image")

shot("1", id="1.8", title="Chief: 'Every month is a bad month.'", who=["chief"],
 frame="Medium close-up of Chief facing three-quarters toward the camera at the window, phone up, flat cold expression.",
 scene="The father answers flatly.",
 focus="Chief's face, centre frame.",
 dialogue=[("0:02-0:05", "chief", "Every month is a bad month.")],
 timeline=[("0:00-0:02", "Chief stares at the screen, expressionless."), ("0:02-0:05", "He says the line flat and cold."), ("0:05-0:10", "He holds the stare without blinking.")],
 camera="Static.", start="New image")

shot("1", id="1.9", title="Segun: 'Christmas. I promise.'", who=["chief", "segun"],
 frame="Close-up over Chief's shoulder onto the phone screen: Segun smiling quickly, someone calling him off-screen in his office.",
 scene="The son makes another promise.",
 focus="The phone screen, Segun's face.",
 dialogue=[("0:01-0:05", "phone:segun", "Christmas. I promise. We'll all come at Christmas.")],
 timeline=[("0:00-0:01", "Segun looks back at the camera on the screen."), ("0:01-0:05", "Segun's voice plays from the phone, quick and hopeful."), ("0:05-0:10", "Chief's beard in the foreground stays still.")],
 camera="Static close-up on the phone.", start="New image")

shot("1", id="1.10", title="Chief: 'You promised last Christmas.'", who=["chief"],
 frame="Close-up of Chief's face by the window, eyes wet, lamp light on his cheek.",
 scene="The father reminds his son of a broken promise.",
 focus="Chief's eyes, centre frame.",
 dialogue=[("0:02-0:05", "chief", "You promised last Christmas.")],
 timeline=[("0:00-0:02", "Chief is silent, his eyes filling."), ("0:02-0:05", "He says the line quietly, barely holding his voice steady."), ("0:05-0:10", "A tear gathers; he does not let it fall.")],
 camera="Very slow push-in.", start="New image")

shot("1", id="1.11", title="Segun hangs up", who=["chief", "segun"],
 frame="Close-up over Chief's shoulder onto the phone screen: Segun waving quickly, already turning away.",
 scene="The son ends the call in a hurry.",
 focus="The phone screen, then Chief's still beard.",
 dialogue=[("0:01-0:05", "phone:segun", "Daddy, they're calling me in. I love you. Bye-bye!")],
 timeline=[("0:00-0:01", "Segun waves on the screen."), ("0:01-0:05", "Segun's voice plays from the phone, hurried."), ("0:05-0:07", "The video on the screen freezes and goes still."), ("0:07-0:10", "Chief's hand holding the phone starts to shake.")],
 camera="Static close-up on the phone.", start="New image")

shot("1", id="1.12", title="The phone hits the marble", who=["chief"],
 frame="Low-angle medium shot of Chief by the window raising the phone in anger, lamp light behind him, rain on the window.",
 scene="The old man's hurt turns to rage.",
 focus="Chief's arm and the phone, centre frame.",
 dialogue=[],
 timeline=[("0:00-0:02", "Chief stares at the frozen phone, breathing hard."), ("0:02-0:04", "He throws the phone down onto the marble floor."), ("0:04-0:06", "The screen cracks; small pieces of glass scatter."), ("0:06-0:10", "He stands over it, chest heaving, leaning on his cane.")],
 camera="Static low angle.", start="New image")

shot("1", id="1.13", title="After-action: the broken phone", who=["chief"],
 frame="Low close-up on the marble floor: the cracked phone among small pieces of glass, Chief's feet and the tip of his ivory cane softly blurred behind it.",
 scene="The broken phone on the floor; the silence after the anger.",
 focus="The cracked phone in the centre foreground.",
 dialogue=[],
 timeline=[("0:00-0:04", "The cracked phone lies still; rain taps the window."), ("0:04-0:07", "The cane tip shifts slightly behind it."), ("0:07-0:10", "Chief's heavy breathing slowly calms.")],
 camera="Static, very low to the floor.", start="New image")

shot("1", id="1.14", title="Nurse Grace rushes in", who=["grace", "chief"],
 frame="Medium shot from inside the bedroom: Nurse Grace has just stepped through the open door, worried, facing the camera; Chief by the window at the edge of the frame with his back half turned; the broken phone on the floor between them.",
 scene="The nurse hears the crash and rushes in.",
 focus="Nurse Grace in the doorway, centre frame.",
 dialogue=[("0:01-0:04", "grace", "Sir! Sir, is everything okay?")],
 timeline=[("0:00-0:01", "Grace steps in quickly."), ("0:01-0:04", "She speaks, worried."), ("0:04-0:10", "She looks from the broken phone to Chief, waiting.")],
 camera="Static medium shot.", start="New image")

shot("1", id="1.15", title="Chief: 'Leave my room.'", who=["chief", "grace"],
 frame="Medium close-up of Chief by the window in three-quarter view, not looking at her, jaw tight; Grace soft in the background by the door.",
 scene="The old man dismisses the nurse.",
 focus="Chief's face in the foreground.",
 dialogue=[("0:02-0:04", "chief", "Leave my room.")],
 timeline=[("0:00-0:02", "Chief keeps staring at the window."), ("0:02-0:04", "He says the line without turning, low and cold."), ("0:04-0:10", "Behind him, Grace hesitates, then steps closer.")],
 camera="Static.", start="New image")

shot("1", id="1.16", title="Grace: 'Let me help you'", who=["grace", "chief"],
 frame="Medium two-shot: Grace beside Chief by the window, facing the camera at three-quarters, gently reaching for his elbow; Chief in profile.",
 scene="The nurse gently tries to help him.",
 focus="Grace's face and her hand reaching for his elbow.",
 dialogue=[("0:01-0:06", "grace", "Sir, your blood pressure. Please, let me help you to the chair…")],
 timeline=[("0:00-0:01", "Grace steps beside him."), ("0:01-0:06", "She speaks softly and kindly."), ("0:06-0:10", "She gently takes his elbow.")],
 camera="Slow, gentle push-in.", start="New image")

shot("1", id="1.17", title="Chief: 'Don't touch me!'", who=["chief", "grace"],
 frame="Medium two-shot: Chief turning on Grace with fury, facing the camera; Grace at the edge of the frame by the dark wood dresser.",
 scene="The old man explodes at the nurse.",
 focus="Chief's furious face, centre frame.",
 dialogue=[("0:02-0:07", "chief", "Don't touch me! Why are you here? Because I pay you!")],
 timeline=[("0:00-0:02", "Chief pulls his arm free and pushes her hand away; she steps back against the dresser, unhurt."), ("0:02-0:07", "He shouts the line, shaking with anger."), ("0:07-0:10", "He breathes hard, glaring.")],
 camera="Static.", start="New image")

shot("1", id="1.18", title="Chief: 'Paid to forget me'", who=["chief", "grace"],
 frame="Medium shot of Chief pointing his ivory cane toward Grace (at the edge of the frame), lamp light hard on his face.",
 scene="He accuses everyone, even his children, of being paid to care.",
 focus="Chief's face and the raised cane.",
 dialogue=[("0:01-0:08", "chief", "Everybody in this house is paid to smile at me. My children too. Paid with my money to forget me!")],
 timeline=[("0:00-0:01", "Chief raises the cane."), ("0:01-0:08", "He speaks with bitter anger, voice rising on 'forget me'."), ("0:08-0:10", "He keeps the cane pointed, trembling.")],
 camera="Static.", start="New image")

shot("1", id="1.19", title="Chief: 'Go home to your own father'", who=["chief", "grace"],
 frame="Close-up of Chief with the cane still raised, breathing hard; Grace blurred by the dresser behind.",
 scene="He says something cruel he will regret.",
 focus="Chief's face, centre frame.",
 dialogue=[("0:01-0:07", "chief", "Go home to your own father, if he's still alive, and see whether you'll even visit him.")],
 timeline=[("0:00-0:01", "Chief glares."), ("0:01-0:07", "He says the line cold and cruel."), ("0:07-0:10", "In the background, Grace freezes.")],
 camera="Static close-up.", start="New image")

shot("1", id="1.20", title="Grace: 'My father is dead, sir.'", who=["grace", "chief"],
 frame="Close-up of Grace against the dresser, straightening slowly, tears in her eyes, facing the camera; Chief soft in the background.",
 scene="The nurse quietly tells him her father is dead.",
 focus="Grace's face, centre frame.",
 dialogue=[("0:03-0:05", "grace", "My father is dead, sir.")],
 timeline=[("0:00-0:03", "Silence. Grace slowly straightens up, tears falling."), ("0:03-0:05", "She says the line quietly."), ("0:05-0:10", "Behind her, Chief's face flickers with shame; he opens his mouth slightly but no words come.")],
 camera="Static close-up.", start="New image")

shot("1", id="1.21", title="The badge on the dresser", who=["grace", "chief"], ref=["grace", "chief"],
 frame="Close shot of Grace's hands unpinning the small name badge from the chest of her navy scrubs, just above the dark wood dresser top, her chin and the lower part of her face softly visible at the top of the frame, warm lamp light on her hands.",
 scene="Humiliated and grieving, the nurse quietly quits: she takes off her name badge, leaves it on the dresser and walks out with her dignity.",
 focus="Grace: first her trembling hands and the badge, then her tear-streaked face as she turns to leave.",
 dialogue=[], timeline=[("0:00-0:03", "Grace's fingers tremble as she slowly unpins the name badge from her scrubs."), ("0:03-0:05", "She places the badge gently on the dresser and rests her fingertips on it for one second."), ("0:05-0:07", "The camera tilts up to her face: tears on her cheeks, lips pressed together, she breathes in and lifts her chin with dignity."), ("0:07-0:10", "She turns and walks out through the open door without looking back. Behind her, Chief stands still with his head lowered.")],
 camera="Static close shot on her hands, then a slow, smooth tilt up to her face at 0:05, then the camera stays still as she walks away.",
 sound="her soft unsteady breath, the tiny click of the badge on the wood, her footsteps leaving on the marble, rain on the windows, a clock ticking", start="New image")

shot("1", id="1.22", title="Aunty Ronke and the blue tablet", who=["ronke", "chief"],
 frame="Aunty Ronke standing in the open doorway facing the camera, holding a silver tray with a glass of water and one small blue tablet; Chief in the foreground in profile.",
 scene="The housekeeper brings the evening tablet.",
 focus="Ronke and the silver tray, centre frame.",
 dialogue=[("0:01-0:07", "ronke", "Your evening tablet, sir. You've been shouting. It's for your pressure.")],
 timeline=[("0:00-0:01", "Ronke steps in calmly."), ("0:01-0:07", "She speaks, polite and cold."), ("0:07-0:10", "She holds out the tray.")],
 camera="Slow, gentle push-in on Ronke.", start="New image")

shot("1", id="1.23", title="She watches him swallow", who=["ronke", "chief"],
 frame="Over Chief's shoulder onto Ronke's face as he drinks from the glass; her eyes fixed on him.",
 scene="She watches him take the tablet a moment too long.",
 focus="Ronke's eyes.",
 dialogue=[],
 timeline=[("0:00-0:03", "Chief swallows the blue tablet and drinks."), ("0:03-0:06", "Ronke watches him swallow without blinking, a beat too long."), ("0:06-0:10", "She steps back out and slowly closes the door. The door stays closed.")],
 camera="Static.", start="New image")

shot("1", id="1.24", title="Grace, come back", who=["chief"],
 frame="Chief alone at the dresser in three-quarter view, looking down at Grace's name badge in his hand; his face softening.",
 scene="Alone, the old man regrets what he said.",
 focus="Chief's face and the badge in his hand.",
 dialogue=[],
 timeline=[("0:00-0:04", "Chief looks at the badge; his hard face softens."), ("0:04-0:07", "He sets it down gently."), ("0:07-0:10", "He turns and limps slowly toward the door with his cane.")],
 camera="Slow, gentle push-in.", start="New image")

shot("1", id="1.25", title="Top of the twenty-two steps", who=["chief"],
 frame="Wide shot from halfway down the grand curved marble staircase looking up: Chief at the top, one hand on the banister, cane in the other, facing down toward the camera, the dim chandelier above him.",
 scene="He calls down the staircase for the nurse.",
 focus="Chief at the top of the stairs, centre frame.",
 dialogue=[("0:01-0:06", "chief", "Grace… Grace, come back. I didn't mean…")],
 timeline=[("0:00-0:01", "Chief grips the banister."), ("0:01-0:06", "He calls down, almost gently."), ("0:06-0:10", "He blinks hard and sways slightly.")],
 camera="Static wide.", start="New image")

shot("1", id="1.26", title="His vision blurs", who=[],
 frame="Point-of-view shot from the top of the staircase looking down the 22 marble steps, the chandelier glowing at the top of frame, slightly soft focus.",
 scene="The drug takes hold: his vision swims.",
 focus="The steps and the chandelier.",
 dialogue=[],
 timeline=[("0:00-0:04", "The view slowly drifts out of focus."), ("0:04-0:08", "The image gently tilts to one side; the chandelier light swims."), ("0:08-0:10", "Heavy breathing is heard.")],
 camera="Slow drifting tilt, soft focus.", start="New image")

shot("1", id="1.27", title="The fall (5 seconds)", who=["chief"], dur=5,
 frame="Wide shot from the bottom of the grand curved white marble staircase looking up: Chief at the top step caught at the exact moment he loses his balance, his ivory cane sliding out from under him on the polished marble, his body tipping forward and sideways, one hand reaching for the banister and missing, his face visible with shock in his eyes; the dim chandelier above him, the huge portrait at the bottom of the frame.",
 scene="An elderly man in a white kaftan loses his balance at the top of a grand marble staircase and falls all the way down to the bottom.",
 focus="Chief's whole body as he falls, centre frame, from the top step to the bottom of the stairs.",
 dialogue=[("0:00-0:02", "chief", "Aaah! Aaaah!"), ("0:04-0:05", "chief", "Mmh…")], timeline=[("0:00-0:01", "His ivory cane slides out from under him on the polished marble. His eyes fly wide open in shock, his mouth opens and he cries out. His knees buckle, his body pitches forward, his hand grabs for the banister and misses."), ("0:01-0:04", "Shouting in fear and pain, he falls hard onto his side and tumbles down the curved staircase, rolling over the steps, arms flailing, face twisted in pain, his kaftan twisting around him. The cane bounces and clatters down the steps ahead of him."), ("0:04-0:05", "He lands at the bottom on the marble floor beneath the portrait, lets out one weak groan, his face creased in pain, then goes completely still. The cane rolls to a stop beside him. No blood, no injuries shown.")],
 camera="Static wide shot from the bottom of the staircase looking up, the whole staircase in frame so the full fall is seen. Real-time speed with weight and gravity, a slight slow motion only on the first moment he tips forward.",
 extra_look="Real body weight and physics: he truly falls, he does not float, glide or slide gently. Strong, real facial expression the whole way: shock, fear and pain.",
 sound="his loud cry of shock and pain, the cane clattering down the marble steps, the dull thuds of his body on the stairs, his weak groan at the bottom, rain on the windows, distant thunder", start="New image")

shot("1", id="1.28", title="Beneath Mama Abike's portrait", who=["chief"],
 frame="Low close shot along the marble floor: Chief lying still at the foot of the staircase, eyes half closed, the huge portrait of the smiling woman in the gold gele above him.",
 scene="He lies beneath his late wife's portrait.",
 focus="Chief's face and his reaching fingers.",
 dialogue=[],
 timeline=[("0:00-0:04", "Silence except rain. Chief lies still."), ("0:04-0:07", "His fingers twitch and slowly reach toward the portrait, then stop."), ("0:07-0:10", "The camera rises slowly to the portrait's smiling face.")],
 camera="Static, then a slow rise up to the portrait.", start="New image")

shot("1", id="1.29", title="She waits", who=["ronke"],
 frame="Looking up from the bottom of the stairs into the dark upstairs corridor: a door opened a crack, half of Aunty Ronke's face visible, watching.",
 scene="The housekeeper watches from the dark and does nothing.",
 focus="Ronke's half-hidden face in the door gap.",
 dialogue=[],
 timeline=[("0:00-0:06", "Ronke watches without moving, without screaming."), ("0:06-0:10", "She stays still as the image slowly fades to black.")],
 camera="Very slow push-in, then fade to black.", start="New image")

# ---------------- SCENE 2 ----------------
shot("2", id="2.1", title="Ambulance in the rain", who=[],
 frame="Exterior of a sleek private hospital in Ikoyi at night, rain falling, an ambulance at the entrance with its blue light flashing softly on the wet ground.",
 scene="That night, an ambulance arrives at a private hospital in the rain.",
 focus="The ambulance at the entrance, centre frame.",
 dialogue=[], timeline=[("0:00-0:04", "Rain falls; the blue light pulses softly on the wet ground."), ("0:04-0:07", "A paramedic closes the ambulance door."), ("0:07-0:10", "The camera keeps moving slowly toward the entrance.")],
 camera="Slow push toward the entrance.", start="New image")

shot("2", id="2.2", title="Femi bursts in", who=["femi", "chief", "gabriel", "hassan"],
 frame="Medium shot inside the VIP suite: Femi has just come through the door facing the camera, tie loose, two phones in his hand; Gabriel behind him; Dr. Hassan by the lightbox; Chief unconscious in the bed in the foreground.",
 scene="The billionaire's grandson rushes into the hospital room.",
 focus="Femi in the doorway, centre frame.",
 dialogue=[("0:01-0:04", "femi", "Doctor, talk to me. How bad?")],
 timeline=[("0:00-0:01", "Femi strides in."), ("0:01-0:04", "He speaks urgently to the doctor."), ("0:04-0:10", "Dr. Hassan turns from the lightbox holding an X-ray; Gabriel stays by the door.")],
 camera="Static medium shot.", start="New image")

shot("2", id="2.3", title="The X-ray", who=["hassan", "femi"],
 frame="Medium two-shot: Dr. Hassan facing the camera, pointing at an X-ray on the lightbox; Femi beside him in profile, tense.",
 scene="The doctor explains the injury.",
 focus="Dr. Hassan's face and the X-ray.",
 dialogue=[("0:01-0:09", "hassan", "He fractured his hip, and the fall bruised his lower spine. There's severe swelling around the nerves.")],
 timeline=[("0:00-0:01", "Dr. Hassan points at the X-ray."), ("0:01-0:09", "He explains calmly and seriously."), ("0:09-0:10", "He lowers the X-ray.")],
 camera="Slow, gentle push-in.", start="New image")

shot("2", id="2.4", title="'Your grandfather will not walk again.'", who=["hassan", "femi"],
 frame="Close-up of Dr. Hassan facing Femi, three-quarters to the camera, grave and honest; Femi soft at the edge of the frame.",
 scene="The doctor delivers the worst news.",
 focus="Dr. Hassan's face, centre frame.",
 dialogue=[("0:01-0:08", "hassan", "Mr. Adenuga, I'll be honest with you. From what I see tonight, your grandfather will not walk again.")],
 timeline=[("0:00-0:01", "Dr. Hassan takes a breath."), ("0:01-0:08", "He speaks gently and clearly."), ("0:08-0:10", "He holds Femi's gaze.")],
 camera="Static close-up.", start="New image")

shot("2", id="2.5", title="After-action: Femi hears it", who=["femi"],
 frame="Close-up of Femi's face, stunned, the two phones in his hand below frame.",
 scene="The grandson is struck by the news.",
 focus="Femi's eyes.",
 dialogue=[],
 timeline=[("0:00-0:03", "Femi's phones buzz in his hand."), ("0:03-0:06", "The buzzing slowly stops; he doesn't look at them."), ("0:06-0:10", "He stares, stunned, his breath catching.")],
 camera="Static close-up.", start="New image")

shot("2", id="2.6", title="Femi: 'Germany. America.'", who=["femi", "hassan"],
 frame="Medium close-up of Femi facing the camera, pleading; Dr. Hassan soft at the edge of the frame.",
 scene="The grandson refuses to accept it.",
 focus="Femi's face.",
 dialogue=[("0:01-0:07", "femi", "There must be something. Germany. America. I'll fly in any specialist…")],
 timeline=[("0:00-0:01", "Femi steps toward the doctor."), ("0:01-0:07", "He pleads, fast and desperate."), ("0:07-0:10", "He waits, breathing hard.")],
 camera="Static.", start="New image")

shot("2", id="2.7", title="Dr. Hassan: 'The spine doesn't read passports.'", who=["hassan", "femi"],
 frame="Medium close-up of Dr. Hassan facing the camera, kind but firm; Femi soft at the edge of the frame.",
 scene="The doctor gently tells him money won't fix this.",
 focus="Dr. Hassan's face.",
 dialogue=[("0:01-0:08", "hassan", "You can fly him anywhere in the world, but the spine doesn't read passports. Prepare him.")],
 timeline=[("0:00-0:01", "Dr. Hassan shakes his head slightly."), ("0:01-0:08", "He speaks gently and firmly."), ("0:08-0:10", "He puts a hand briefly on Femi's arm.")],
 camera="Static.", start="New image")

shot("2", id="2.8", title="Chief has heard everything", who=["chief"],
 frame="Close-up of Chief in the hospital bed, his eyes slowly opening, monitor light on his face.",
 scene="The old man wakes and has heard everything.",
 focus="Chief's eyes.",
 dialogue=[],
 timeline=[("0:00-0:04", "Chief's eyes slowly open."), ("0:04-0:08", "He stares at the ceiling; he has heard everything."), ("0:08-0:10", "One slow breath.")],
 camera="Static close-up.", start="New image")

shot("2", id="2.9", title="Femi: 'I'm here.'", who=["femi", "chief"],
 frame="Medium shot: Femi sitting on the edge of the bed facing the camera, holding his grandfather's hand in both of his; Chief in the bed in profile.",
 scene="The grandson promises his grandfather everything will be fine.",
 focus="Femi's face and their hands.",
 dialogue=[("0:01-0:07", "femi", "Grandpa. I'm here. Everything will be fine. I promise you.")],
 timeline=[("0:00-0:01", "Femi squeezes the hand."), ("0:01-0:07", "He speaks softly, close to tears."), ("0:07-0:10", "He waits for a response.")],
 camera="Slow, gentle push-in.", start="New image")

shot("2", id="2.10", title="He turns his face to the wall", who=["chief", "femi"],
 frame="Close shot over Femi's shoulder onto Chief's face on the pillow.",
 scene="The old man turns away from his grandson.",
 focus="Chief's face turning away.",
 dialogue=[],
 timeline=[("0:00-0:03", "Chief looks at the hands holding his."), ("0:03-0:07", "Slowly and deliberately, he turns his face away to the wall."), ("0:07-0:10", "His hand stays limp; Femi's shoulders drop.")],
 camera="Static.", start="New image")

shot("2", id="2.11", title="Lekan arrives with lilies", who=["lekan", "chief", "ronke"],
 frame="Medium shot: Lekan entering through the door with a huge bouquet of white lilies, facing the camera; Aunty Ronke in the corner holding an overnight bag; the bed in the foreground.",
 scene="The company's vice-chairman arrives, too friendly.",
 focus="Lekan and the lilies, centre frame.",
 dialogue=[("0:01-0:09", "lekan", "Chief! Ah! God forbid bad thing! Rest, Chief. Rest. Femi and I will carry the company.")],
 timeline=[("0:00-0:01", "Lekan sweeps in."), ("0:01-0:09", "He speaks loud and warm, putting the flowers down and patting the blanket."), ("0:09-0:10", "His smile holds.")],
 camera="Static medium shot.", start="New image")

shot("2", id="2.12", title="The secret nod", who=["lekan", "ronke"],
 frame="Medium shot across the room: Lekan by the bed and Aunty Ronke in the corner, their eyes meeting.",
 scene="A secret signal passes between the two plotters.",
 focus="Ronke's eyes, then Lekan's.",
 dialogue=[],
 timeline=[("0:00-0:03", "Lekan glances at Ronke."), ("0:03-0:05", "The smallest nod passes between them."), ("0:05-0:10", "Ronke looks down at the bag; the monitor beeps steadily.")],
 camera="Slow pan from Lekan to Ronke.", start="New image")

shot("2", id="2.13", title="Femi calls his father", who=["femi", "gabriel"],
 frame="Hospital corridor: Femi facing the camera with a phone to his ear, Gabriel leaning against the wall behind him; through the glass wall, Chief in bed facing the wall.",
 scene="The grandson calls his father with the news.",
 focus="Femi's face, centre frame.",
 dialogue=[("0:01-0:08", "femi", "Dad, he fell down twenty-two steps. He can't walk. You're not coming?")],
 timeline=[("0:00-0:01", "Femi paces into frame, phone to ear."), ("0:01-0:08", "He speaks, his voice breaking on the question."), ("0:08-0:10", "He stops and listens.")],
 camera="Static.", start="New image")

shot("2", id="2.14", title="Segun on the phone: 'Money is not the problem.'", who=["femi", "gabriel"],
 frame="Close-up of Femi with the phone to his ear, listening, face hardening; Gabriel soft behind him.",
 scene="The father answers from far away, offering only money.",
 focus="Femi's face as he listens.",
 dialogue=[("0:01-0:07", "phone:segun", "Hire the best caretaker in Lagos, Femi. Pay anything. Money is not the problem.")],
 timeline=[("0:00-0:01", "Femi listens."), ("0:01-0:07", "Segun's voice plays from the phone at Femi's ear."), ("0:07-0:10", "Femi slowly lowers the phone, jaw tight.")],
 camera="Static close-up.", start="New image")

shot("2", id="2.15", title="Femi: 'Money is the only thing…'", who=["femi", "gabriel"],
 frame="Two-shot in the corridor: Femi facing the camera, bitter; Gabriel beside him in three-quarter view.",
 scene="The grandson speaks the bitter truth to his friend.",
 focus="Femi's face.",
 dialogue=[("0:01-0:06", "femi", "Money is the only thing in this family that's never the problem.")],
 timeline=[("0:00-0:01", "Femi turns to Gabriel."), ("0:01-0:06", "He speaks quietly and bitterly."), ("0:06-0:10", "Gabriel puts a hand on his shoulder.")],
 camera="Slow, gentle push-in.", start="New image")

shot("2", id="2.16", title="Through the glass", who=["chief"],
 frame="View through the glass wall of the hospital room: Chief in the bed, staring at the wall, small and alone.",
 scene="The old man alone, staring at the wall.",
 focus="Chief in the bed.",
 dialogue=[],
 timeline=[("0:00-0:06", "Chief lies still, staring at the wall."), ("0:06-0:10", "The image slowly fades.")],
 camera="Very slow push toward the glass, then fade.", start="New image")
