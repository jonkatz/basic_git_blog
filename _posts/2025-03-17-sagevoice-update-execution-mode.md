---
title: " Execution mode!"
date: 2025-03-17 11:29:00
categories: [newsletter]
tags: [mailchimp]
---

# Execution mode!

Right now, I feel like entering execution mode. I have some clear product changes to make before going back into outreach and exploration. But the last two weeks have been eventful!

## Reminder: SageVoice value proposition

**We solve** interviewing subjects at scale, **for** clinical researchers, **by** offering structured interviews **using** AI-enabled telephone calls.

## Request of you

**Does anybody have friends at OpenAI?** I need to get a HIPAA-agreement from them, which is something they do, but they’re not being responsive via standard channels. I could use a friendly ping!  They’re not baked into SageVoice today, but I think using them will improve some issues we saw with the first patients.

## On Deck Founders review

Two weeks ago, I spent the week in SF onboarding for On Deck Founders (ODF).  ODF is more of a community than an experience, and they stressed that this was just a 1-week onboarding with our cohort.  Going in, I was worried it would be douche-y.  It wasn’t!

<img src="{{ site.baseurl }}/assets/images/c84c3e2c-c311-1632-a01b-018856277b89.jpeg" alt="c84c3e2c-c311-1632-a01b-018856277b89.jpeg">

There was an application process, but because they charge for it, I wasn’t sure if it would be valuable. It was! There were some really helpful talks around startup logistics, but the primary value was getting to talk with other founders who were all very impressive. It was inspiring, therapeutic and helped me think through some things.  But I suspect there will be a long-tail of support from the community, which seems really supportive. I’ve already had someone from an earlier cohort reach out to chat, unprompted.

My primary goals were to find a co-founder and get $10k in Amazon Cloud (AWS) credits. The AWS credits are pending.  The cofounder aspect was interesting.  Most people were looking for a cofounder and most people were technical.  The problem is that most people already had ideas they were excited about. The bar is very high for bringing on someone to work with when you are focused on an idea.  It is probably impossible if they have a different idea they’re stoked about. I talked to one founder who said that after her last company she is starting with the cofounder search so that they find an idea together. Coming out of this, that makes a lot of sense to me.

I did find someone I’m excited to work with (👋 Venki!), who is interested in exploring what we can do together. Venki has his own idea and isn’t thrilled with mine, so it’s unlikely we’ll partner in a formal way in the near-term, but it’s great to be reminded of what it feels like to be excited to work with someone.

## First patient contact

On March 7th, the Columbia lab shared the app with its first 2 patients. This was during ODF week, so I was up until 2am the night before testing. It wasn’t a slam dunk, but it wasn’t terrible either. We identified some things to polish. My takehomes were two-fold:

- I’m the worst tester, because I know the system too well. I sub-consciously sidestep issues that a n00b would fall into.
- Short contexts are much harder than interviews.  Sage was trained to be a long-form interviewer and is great at that.  Missing a few words here and there is not a big deal, because there is a lot of context and the AI recovers. With short surveys the mistakes hit harder.  Happy to explain why directly.

We paused last week so that I could polish some things and this week we’re trying another 2 patients.

<img src="{{ site.baseurl }}/assets/images/aa853fcb-e78f-4f3d-063e-ea0abb23e0ab.gif" alt="aa853fcb-e78f-4f3d-063e-ea0abb23e0ab.gif">

## Automated testing

One of the challenges with voice is that there haven’t been good ways to automated testing. You can’t program a bot to run through a series of steps to make sure they work. UNTIL NOW!

I reached out to a company called Hamming.ai (YC 23) who, get this, has their bot call _your_ bot. So I can have 10 fake, grumpy non-technical “people” call the bot and either try to be cooperative or uncooperative. I think it is going to be a game changer!

<img src="{{ site.baseurl }}/assets/images/54dd2d2e-c91e-e06b-31fd-5b43751d07ed.jpeg" alt="54dd2d2e-c91e-e06b-31fd-5b43751d07ed.jpeg">

## Last two weeks

- **Attended ODF:** No big developments, but good vibes and solid investment in my network
- **Customer Development**

  - **First patient roll-out slow trickle.** See above
  - **Stanford Lab is not going to pilot.** The primary advocate at the Stanford lab I was talking to went on sabbatical and now the lab is saying they want the tool, but only after it’s been verified elsewhere.
  - Scheduled meetings (long time in the works) with Stanford Medical research efficiency group and Berkeley Public Health Dean.

- **Product Development:**

  - **Began working on a new cognitive diagnostic for Columbia lab**. This use case is very promising
  - **Fixed some issues** identified from patient rollout with Columbia lab.
  - Improved logging (which degraded when I moved to AWS)
  - Built new patient outreach demo for a large Dementia prevention study in Southern California
  - Setup automated testing

- **HIPAA compliance:**

  - Started developing a HIPAA compliant upload/download tool for getting data in and out
  - Reviewed and finalized 6 of 42 official company HIPAA “policies”

## This week

- **Customer Development**

  - **Demo** for team that runs Dementia Prevention study in Southern California
  - Should I be talking to more potential clients? I should have a steady pipeline going, but I know that HIPAA and some functionality are blockers…so I think I need to nail that down first.

- **Product Development:**

  - Start using GPT4 Realtime to get **improved transcriptions** (use context for better results)
  - Get **new cognitive diagnostic** up and running–requires some new feature work

- **HIPAA**

  - **Gruntwork.** There is a boatload of checking boxes to do here.
  - I will work on the front end if I can.

- **Family fun**

  - Chaperoning a first-grade field trip to the Oakland Zoo.

## Stock Video of the Week

As I mentioned last week, we can now make videos out of a single image.  As a friend said “It’s not the AI future we wanted, but it’s the one we deserve”.

A few weeks ago, I shared this weird image of a woman giving an apple to a horse

<img src="{{ site.baseurl }}/assets/images/a8548558-fd49-e7db-4770-22415741928a.jpg" alt="a8548558-fd49-e7db-4770-22415741928a.jpg">

The guy on the left looks so annoyingly smug and I imagine the guy on the right just hating him.  So I made it into a video:

_A tense newsroom scene unfolds as the reporter in blue (on the right), visibly frustrated, confronts a sneering colleague. The atmosphere is charged with tension as the reporter stands up, his expression a mix of determination and annoyance. He firmly tells the colleague to 'get lost,' emphasizing his point with a wave of his hand. The camera captures the moment as the reporter turns on his heel and walks away, leaving the sneering colleague momentarily stunned._

This worked pretty well:

<img src="{{ site.baseurl }}/assets/images/9bc62d47dd6af4bd888b83b1122825d7.png" alt="9bc62d47dd6af4bd888b83b1122825d7.png">

They offer a lip-syncing option, which did _not_ perform well.

<img src="{{ site.baseurl }}/assets/images/061df5ae775097873f5f31f623a20c9f.png" alt="061df5ae775097873f5f31f623a20c9f.png">

I tried again. I started with this image of Trump and Putin dishing about strongman stuff and made it into video.

<img src="{{ site.baseurl }}/assets/images/390d6023-08aa-e171-4487-78aeb2632d4b.jpg" alt="390d6023-08aa-e171-4487-78aeb2632d4b.jpg">

On the one hand, I’m pleased they let me muck around with a known figure without censoring it.  On the other hand, the lip syncing was pretty lame.

I gave Trump this to say

_I think if we all dig deep within ourselves we'll find that we are made of love. You, me, Peter Pan.  We all have so much love to give._

Not so great.

<img src="{{ site.baseurl }}/assets/images/cc251912ee0d44164dc18cfb7a59782e.png" alt="cc251912ee0d44164dc18cfb7a59782e.png">

So… cheap AI lip syncing out of the box on your first 2 tries: not there yet.

This is actually somewhat relevant to me.  If we want to have a bot with a visual expression, it’s mouth will need to move in a not-terrible way.

**As always, questions/feedback/advice on the process or even this email is welcome!**
