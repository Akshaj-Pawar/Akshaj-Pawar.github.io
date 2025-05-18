import pandas as pd

data = {
    'text': [
        'Today I went for a long run and felt amazing',
        'I walked around the neighborhood with my dog',
        'I did an intense spinning class',
        'Rest day, just did some light stretching',
        'Played tennis with my little brother for most of the afternoon',
        'Rest day in preparation for running a marathon tomorrow',
        'Lifted a few lego bricks',
        'Danced a lot at the club, flushed by the end',
        'Read for a few hours',
        'Did some light stretching',
        'Ten pushups',
        'Managed to swim 4 lengths of the pool',
        'Twenty Pushups',
        'Forty Pushups',
        'Went for a short run around the neighbourhood',
        'I walked around',
        'I did an intense martial arts class',
        'Fenced till I was sore',
        'Rest day',
        'Played tennis for most of the morning',
        'Cycled hard uphill for a good half-hour, then down to the park a few miles away',
        'did 1000 steps throughout the day',
        'did a thousand steps briskly',
        'did 100 steps throughout the day',
        'Danced a lot at home, panting by the end',
        'Read the great gatsby, the pages were not heavy',
        'Did some light-show work',
        'Ten slow situps',
        'Did an intense swimming class',
        'Twenty slow situps',
        'Forty situps without stopping',
        'Today I went for a long jog and felt tired but proud',  # medium
        'I walked around the park with my neighbor',  # low
        'I did a hard spinning class with extra intervals, no breaks',  # high
        'Just rested today and did a few yoga stretches',
        'Played doubles tennis with friends for two hours',  # medium
        'Took a rest day to prepare for tomorrows half-marathon',  # very low
        'Lifted my shopping bags and some books',  # very low
        'Danced at home for a few hours, pretty sweaty by the end', 
        'Read a novel for most of the afternoon',  # very low
        'Did some light morning stretching',  # very low
        'Ten slow pushups with lots of breaks',  # low
        'Swam 6 slow laps at the community pool',  # low
        'Twenty fast pushups', 
        'Forty pushups without stopping',  # high
        'Went for a slow jog around the block', 
        'Strolled around the mall for a bit',  # very low
        'I did an intense kickboxing session',  # high
        'Practiced fencing drills until exhausted',  # high
        'Completely rested today, no activity',  #none
        'Played a tennis match (best of 5 sets) no breaks',  # high
        'Did a gentle yoga class focused on breathing',  # very low
        'Power-walked around the lake for 45 minutes',  # medium
        'Completed a heavy weightlifting session (deadlifts, squats)',  # high
        'Went hiking up a steep mountain trail',  # high
        'Took a slow bike ride around town',  # low
        'Rowed steadily for an hour on a machine',  # medium


        'Sprinted intervals at the track',  # very high
        'Slow danced at a party',  # low
        'Worked in the garden, weeding and planting flowers',  # low

        'Helped a friend move furniture all afternoon',  # medium
        'Did a slow-paced Zumba class',  # medium
        'Practiced tai chi in the park',  # very low
        'Jumped rope lightly for a few minutes',  # medium
        'Did burpees till exhaustion',  # very high
        'Jogged up and down stairs for 10 minutes',  # high
        'Stood and watched my kids soccer game',  # very low
        'Did 30 minutes of Pilates',  # medium
        'Swept and cleaned the house thoroughly',  # low
        'Took a very slow walk to the corner shop',  # very low
        'Ran 10k race at competition pace',  # high
        'Slowly climbed a few flights of stairs',  # low
        'High-intensity spinning followed by slow cooldown ride',  # high
        'Carried groceries home over several blocks',  # medium
        'Did a heavy CrossFit WOD',  # very high
        'Skated around the rink with friends casually',  # low

        'Skated laps competitively at the rink',  # high
        'Did 15 minutes of easy aqua aerobics',  # low
        'Completed a hardcore HIIT session',  # very high
        'Lightly practiced basketball shots with no game',  # low
        'Played a full court basketball game competitively',  # high
        'Did some light stretching after waking up',  # very low

        'Did a moderately intense yoga class',  # medium
        'Power-walked around the park for 45 minutes',  # medium
        'Went hiking down an forest trail, taking occaisonal breaks',  # medium
        'Sprinted around town',  # high
        'Rowed vigorously for an hour on a machine',  # high
        'Worked in the office, selling flowers',  # none
        'Casually practiced cricket in the park',  # medium
        'Jumped rope quickly for thirty minutes',  # high
        'Did burpees till sweating',  # high
        'Slowly climbed a walll at a rock climbing centre',  # medium
        'Carried heavy suitcase home over several blocks',  # medium
        'Skateboarded with friends casually',  # low
        'Did 10 minutes of easy gymnastics',  # low
        'managed to bench press 2 plates for 3 sets of 5 (with 2 second pauses between reps)',
        '3 sets of 5 of 20kg weighted pull ups',
        'managed to do 45kg weighted squats for 3 sets of 20 pain free',
        '3 sets of 10-20 weighted squats with 100kg',
        'almost at 10 pull ups a set', 
        'walking in the gym', 
        'Did Upper Body Row at a weight that impressed the teenage boys in the gym (I am 55 and female)', 
        "was doing lat pulldowns on the planet fitness machines and FINALLY I actually feel it in my lats!", 
        "fast food.", 
        'Hit my best 10k time in 2 years.', 

'Started a running training program last Sunday. Just ran 1.5 miles without stopping. Progress is progress', 

'New PR on my bench press this week. 75kg!', 

'Weight increased from 30 to 45 on most of the machines I use!!!!', 

'Ran 6 miles yesterday, which if someone told me a year ago thats what I could accomplish I would call them nuts!', 

'ran my first 10k without stopping to walk!', 
'Ran 12 miles yesterday even when I wanted to give up',
'I went swimming this week. I wanted to get out of my comfort zone.',

 'Made it to Zumba class, going again today and also on Monday!', 

'I managed a 14km run in my half marathon training and still felt pretty comfortable.', 

'10 long slow miles.', 

"I took out the recycling today!", 

"Woke up with no motivation this morning, but managed to drag my ass to the gym for leg day, and actually managing to have a decent work out?", 

"I moved a few months ago, and finally put together my garage gym at the new place!", 

'on the indoor bike, 10 miles.  Takes about half an hour.',
"Knocked out 4x6 reps of 90kg bench today. Felt strong throughout.",
"Did 3x10 of 15kg weighted pull-ups. Started shaking on the last few reps.",
"Squatted 60kg for 4 sets of 25. Legs officially broken.",
"Hit a solid 10 sets of 10 bodyweight squats for active recovery.",
"Walked 20 minutes to the gym while sipping coffee.",
"Crushed upper body cables today, pushed till failure.",
"Did pulldowns until my lats were sore — felt it even in my core.",
"Ate fast food again, didn't make it to the gym. Tomorrow, maybe.",
"Sprinted a 5k — finished just over 20 minutes. Brutal pace.",
"Jogged 1 mile, walked another 2. Trying to build stamina slowly.",
"Pressed 85kg today — 5 sets of 3. Felt like a PR.",
"Machines felt easy today — added 10kg to every set.",
"Ran 5 miles on an incline treadmill. Soaked in sweat after.",
"10k done in under 50 minutes! Personal best.",
"Long-distance trail run: 18km. Muddy and exhausting but satisfying.",
"First time doing HIIT boxing class. Arms are still shaking.",
"Doubled up cardio today — rowing machine then a 30-minute spin class.",
"14km run. Legs were sore, but I did it.",
"Stretched for 30 minutes. Low-key but still moving.",
"Showed up for leg day but mostly foam rolled and left early.",
"Organized my workout gear at home. Feeling ready for next week.",
"Cycled 15 miles outdoors. Headwinds made it twice as hard.",
"Hill sprints x8 reps — couldnt finish the last one.",
"100 burpees for time. Nearly threw up but finished under 12 minutes.",
"Cranked out 3 sets of 8 reps of 60kg bench press. Felt solid.",
"Did 5 reps of 25kg weighted pull ups. Arms were jelly after.",
"3x15 squats at 80kg — quads on fire by the end.",
"Finally managed 12 pull ups in one set — no breaks.",
"Warm-up walk to the gym, slow pace. Nothing intense.",
"Hit a new high on chest row, the machine maxed out!",
"Got DOMS from lat pulldowns — hit 4 sets of 12 with perfect form.",
"Grabbed fast food again — rest day.",
"Sprint intervals for 20 minutes — felt like dying by the end.",
"Jogged 2 miles without stopping for the first time — pretty happy.",
"Hit 80kg on the bench press today! Personal record!",
"Increased my weights across every machine by at least 20kg.",
"Ran 8 miles in the rain — hardest run of the year.",
"Nonstop 10k today in hilly terrain.",
"14 miles done. Nearly collapsed but I didnt quit.",
"First time swimming laps with intervals — exhausting!",
"Double Zumba day — morning and evening. I'm dead.",
"Ran 16km at race pace — legs were shaking by the end.",
"Walked 7km while talking on the phone.",
"Forced myself to show up for leg day. 4x12 Romanian deadlifts.",
"Finally finished building my home gym — no more excuses.",
"12 miles on the exercise bike, kept my heart rate at 150bpm.",
"Stair sprints — 10 rounds. Thought I might throw up.",
"3 sets of 15 dumbbell thrusters — sweating buckets."
],
    
    'intensity_score': [
        0.65,
        0.15,
        0.75,
        0,
        0.65,
        0,
        0,
        0.35,
        0,
        0.05,
        0.35,
        0.35,
        0.5,
        0.65,
        0.3,
        0.1,
        0.75,
        0.75,
        0,
        0.65,
        0.65,
        0.15,
        0.25,
        0,
        0.65,
        0,
        0,
        0.15,
        0.75,
        0.2,
        0.5,
        0.45,  # medium
        0.1,  # low
        0.85,  # high
        0.05,
        0.55,  # medium
        0,  # very low
        0.05,  # very low
        0.4, 
        0,  # very low
        0.05,  # very low
        0.1,  # low
        0.15,  # low
        0.65, 
        0.75,  # high
        0.1, 
        0.05,  # very low
        0.75,  # high
        0.8,  # high
        0,  #very low
        0.75,  # high
        0.05,  # very low
        0.3,  # medium
        0.8,  # high
        0.8,  # high
        0.1,  # low
        0.5,  # medium
        0.9,  # very high
        0.2,  # low
        0.2,  # low
        0.45,  # medium
        0.4,  # medium
        0.05,  # very low
        0.25,  # medium
        0.85,  # very high
        0.45,  # high
        0,  # very low
        0.5,  # medium
        0.05,  # low
        0.05,  # very low
        0.9,  # high
        0.05,  # low
        0.75,  # high
        0.4,  # medium
        0.9,  # very high
        0.15,  # low
        0.8,  # high
        0.1,  # low
        0.9,  # very high
        0.1,  # low
        0.85,  # high
        0.05,
        0.4,  # medium
        0.25,  # medium
        0.55,  # medium
        0.75,  # high
        0.7,  # high
        0,  # none
        0.6,  # medium
        0.65,  # high
        0.6,  # high
        0.4,  # medium
        0.4,  # medium
        0.05,  # low
        0.1,  # low
        0.55, 0.7, 0.5, 0.75, 0.6, 0.05, 0.85, 0.4, 0.0, 0.85, 0.6, 0.7, 0.6, 0.75, 0.8, 0.85, 0.3, 0.5, 0.75, 0.5, 0.0, 0.5, 0.1, 0.65, 0.55, 0.75, 0.65, 0.7, 0.1, 0.85, 0.6, 0.0, 0.85, 0.15, 0.75, 0.6, 0.65, 0.8, 0.85, 0.8, 0.8, 0.75, 0.15, 0.1, 0.0, 0.65, 0.85, 0.9, 0.6, 0.75, 0.65, 0.7, 0.1, 0.8, 0.6, 0.0, 0.85, 0.55, 0.75, 0.65,
0.9, 0.85, 0.95, 0.7, 0.75, 0.9, 0.2, 0.65, 0.1, 0.6, 0.9, 0.8]
}

print(len(data['text']))
print(len(data['intensity_score']))

# Convert to a DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('journal_entries.csv', index=False)
