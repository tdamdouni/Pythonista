# Where are we in the Python 3 transition?

_Captured: 2016-01-02 at 14:05 from [www.snarky.ca](http://www.snarky.ca/the-stages-of-the-python-3-transition)_

![104_0419_large](https://silvrback.s3.amazonaws.com/uploads/cf71bbc7-e611-4b13-80a1-7c2326bb4d91/104_0419_large.JPG)

The [Kubler-Ross model](https://en.wikipedia.org/wiki/K%C3%BCbler-Ross_model) outlines the stages that one goes through in dealing with death:

  1. Denial
  2. Anger
  3. Bargaining
  4. Depression
  5. Acceptance

This is sometimes referred to as the _five stages of grief_.Some have [jokingly called them the five stages of software development](https://twitter.com/nselby/status/680180690030325760). I think it actually matches the Python community's transition to Python 3 rather well, both what has occurred and where we currently are (summary: the community is at least in stage 4 with some lucky to already be at the end in stage 5).

# Denial

When Python 3 first came out and we said Python 2.7 was going to be the last release of Python 2, I think some people didn't entirely believe us. Others believed that Python 3 didn't offer enough to bother switching to it from Python 2, and so they ignored Python 3's existence. Basically the Python development team and people willing to trust that Python 3 wasn't some crazy experiment that we were going to abandon, ported their code to Python 3 while everyone else waited.

# Anger

When it became obvious that the Python development team was serious about Python 3, some people got really upset. There were accusations of us not truly caring about the community and ignoring that the transition was hurting the community irreparably. This was when whispers of forking Python 2 to produce a Python 2.8 release came about, although that obviously never occurred.

# Bargaining

Once people realized that being mad about Python 3 wasn't going to solve anything, the bargaining began. People came to the Python development team asking for features to be added to Python 3 to make transitioning easier such as bringing back the `u` string prefix in Python 3. People also made requests for exceptions to Python 2's "no new features" policy which were also made to allow for Python 2 to stay a feasible version of Python longer while people transitioned (this all landed in [Python 2.7.9](https://www.python.org/downloads/release/python-279/)). We also extended the maintenance timeline of Python 2.7 from 5 years to 10 years to give people until 2020 to transition before people will need to pay for Python 2 support (as compared to the free support that the Python development team has provided).

# Depression

7 years into the life of Python 3, it seems a decent amount of people have reached the point of depression about the transition. With Python 2.7 not about to be pulled out from underneath them, people don't feel abandoned by the Python development team. Python 3 also has enough new features that are simply not accessible from Python 2 that people want to switch. And with [porting Python 2 code to run on Python 2/3 simultaneously](https://docs.python.org/3/howto/pyporting.html) heavily automated and being doable on a per-file basis, people no longer seem to be adverse to porting their code like they once were (although it admittedly still takes some effort).

Unfortunately people are running up against the classic problem of lacking buy-in from management. I regularly hear from people that they would switch if they could, but their manager(s) don't see any reason to switch and so they can't (or that they would do per-file porting, but they don't think they can convince their teammates to maintain the porting work). This can be especially frustrating if you use Python 3 in personal projects but are stuck on Python 2 at work. Hopefully Python 3 will continue to offer new features that will eventually entice reluctant managers to switch. Otherwise financial arguments might be necessary in the form of pointing out that porting to Python 3 is a one-time cost while staying on Python 2 past 2020 will be a perpetual cost for support to some enterprise provider of Python and will cost more in the long-term (e.g., paying for RHEL so that someone supports your Python 2 install past 2020). Have hope, though, that you can get buy-in from management for porting to Python 3 since others have and thus reached the "acceptance" stage.

# Acceptance

While some people feel stuck in Python 2 at work and are "depressed" over it, others have reached the point of having transitioned their projects and accepted Python 3, both at work and in personal projects. Various numbers I have seen this year suggest about 20% of the scientific Python community and 20% of the Python web community have reached this point (I have yet to see reliable numbers for the Python community as a whole; PyPI is not reliable enough for various reasons). I consistently hear from people using Python 3 that they are quite happy; I have yet to hear from someone who has used Python 3 that they think it is a worse language than Python 2 (people are typically unhappy with the transition process and not Python 3 itself).

With five years left until people will need to pay for Python 2 support, I'm glad that the community seems to have reached either the "depression" or "acceptance" stages and has clearly moved beyond the "bargaining" stage. Hopefully in the next couple of years, managers across the world will realize that switching to Python 3 is worth it and not as costly as they think it is compared to having to actually pay for Python 2 support and thus more people will get to move to the "acceptance" stage.
