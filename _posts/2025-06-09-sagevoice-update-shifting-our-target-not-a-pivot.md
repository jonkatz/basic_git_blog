---
title: " Shifting Our Target (not a pivot)"
date: 2025-06-09 11:52:00
categories: [newsletter]
tags: [mailchimp]
---

Heya Friend,

We’re finally, mostly unpacked.  There’s definitely a bike in my office, but in zoom terms I think the hair maintenance situation is probably the bigger issue.  Do not write me to confirm 😉

<img src="{{ site.baseurl }}/assets/images/b635ac03-b6ac-d37b-8746-e08b5f9b8d59.gif" alt="b635ac03-b6ac-d37b-8746-e08b5f9b8d59.gif">

## Welcome to Saalem!

I mentioned last time that we had 3 new people working on SageVoice and introduced 2 of them.

Our intern, Saalem, started last week.  Saalem is a CS major and Senior at UC Berkeley and will be working with us this summer (and hopefully beyond).  Thanks to Aaron for referring Saalem to us!

## Reminder: Our core value proposition,

**\*We solve** interviewing subjects at scale, **for** clinical researchers, **by** offering structured interviews **using** AI-enabled telephone calls.\*

## GTM shifting

Our recent hypothesis was to start with:

1. Using the bot to collect patient data during a trial, because that seemed like an area we could provide a more unique value proposition.
2. Start with big pharma clinical trial sponsors, because they hold the purse strings and can have say over more of the clinical trial ops than anyone.

But in my outreach, I’m finding that a) patient screening at the front end feels like a lower risk, more urgently felt need and b) smaller companies are easier to connect with.

Working with Hugo now, who has relationships with clinical sites (they recruit and host clinical studies on behalf of pharmaceutical companies), it seems like they are hungry for solutions in this space.

So right now, we’re experimenting with this value proposition:

**\*We solve** screening study participants, **for** clinical trial sites, **by** offering structured interviews **using** AI-enabled telephone calls.\*

For anyone who remembers the options, it’s this one:

<img src="{{ site.baseurl }}/assets/images/0a1d9b57-c6e0-a889-667f-0689eb6a2c7d.png" alt="0a1d9b57-c6e0-a889-667f-0689eb6a2c7d.png">

## Last week

- **Market Exploration and Development.**

  - Goal: With Hugo on board, we have a few warm leads.  This means we needed to put together sales materials.
  - Outputs:

    - 1 pager for site networks
    - Revised demo deck

  - 1 validating interview with a site–they were very interested in a future solution (that got through their security team).

- **Product development**

  - Onboarding Saalem- Saalem is working on our client dashboard and has already made great progress showing stats and the like.
  - Added background voice cancellation.  This is an incredibly important feature for the many users who have a TV on when they pick up, or are in a room with other people talking.
  - Finished migrating to Google Cloud. In the search for better speed, quality and consistency we’ve been experimenting with different services. At one point in the last two weeks had experiments that resulted in 6 different options being played with at once: websocket v. webrtc, anthropic v. gemini, telnyx v. twilio, google v. aws v pipecloud.  Now we have one, coherent system again! I’ll share a system diagram at some point soon.

- **Finished unpacking (others in my house would disagree)**

  - I notably did not donate any home videos to Goodwill _last_ week!

## This week

- **Market Exploration and Development.**

  - **Lead followup:**

    - I’m hoping one or two of Hugo’s leads bear fruit and require follow up
    - I also have scheduled circle backs with leadership at two academic research institutions that had expressed interest (one politely interested, the other seemed enthusiastic)

  - I’m hoping to start putting more time into this space in the coming weeks.

- **Product Development**

  - **Pilot prep:**

    - **Prompt engineering fixes.**  Moving from Anthropic to Google’s LLM led to some hiccups. We moved because Google was faster, but it also seems a bit more likely to deviate from instructions
    - _Maybe next week:_ **Automated-test development.**  Right now my automated tests are organic in that I run some generic bots against ours and view the transcripts.  I want to set up specific tests for it, specifically around areas where the bot is more challenged.

  - **Supporting sales**

    - **Solid dashboard.** Our current, client-facing dashboard is a little janky. Saalem has some features to add and then it’s cleanup time!
    - **Demo video.** Our Columbia pilot lead is presenting on AI at a future-of-research type conference and asked for a 20 second video that showcases the possibilities.

## Media Generation of the Week

While we wait for Veo3 the latest and greatest video generation tool to become more widely available (it’s currently $130 a month), I played around with what we have, inserting my new adorable “Sage” into a favorite movie moment of mine:

<iframe width="560" height="315" src="https://www.youtube.com/embed/Oij4KgZVm8k" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Pretty exciting, reveal, right?

**As always, questions/feedback/advice on the process or even this email is welcome!**
