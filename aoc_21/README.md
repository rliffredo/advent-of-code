## AoC 2021

This year was one of the best since I started doing Advent of Code.  
The quizzes have been mostly interesting yet not too expensive in terms of
time, with the exception maybe of the last week; in general, the challenge
level was increasing every week, with a steeper increase on the last one.  
This year I was not able to make any "decent" classification, but I think this
is normal, given now the huge success of AoC and the amount of people
participating. On the plus side, my sleep deficit never increased too much :)

Unfortunately, I failed my goal to blog about it every day, so I will try to
put something from my memory.


### Day 1: Sonar Sweep

A nice start. The first part, just an application of the pairwise iterator,
which is maybe the most used of the itertools recipes. As a matter of facts,
since python 3.x, it's part of the standard library as cxx, but I already have
it as part of the "common" tools, so I still used the recipe version.  
The second part was just an implementation of the moving average. I am pretty
sure there is already something like that, still I found it easier to implement
it myself.  
As a matter of facts, there _is_ a recipe for the moving average
[using deque][1] and itertools:

```python
from collections import deque
import itertools

def moving_average(iterable, n=3):
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    # https://en.wikipedia.org/wiki/Moving_average
    it = iter(iterable)
    d = deque(itertools.islice(it, n-1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / n
```

### Day 2: Dive!

The second day reminded me of classic AoC puzzles, but it was still on the
easy side.  
The problem were very similar -- which is not so common in AoC, with the second
being just a small complication on the first. Still, I was able to use the same
approach in both, which involved using the command pattern.

I am describing the solution as "command pattern", but I used an imperative
approach, with no OO. Not that OO would have bee na bad idea; but of AoC it's
usually slower in the implementation, with no discernible advantages. Still, I
think the concept was the same, with just a different way of dispatching, so I
am still using the "command pattern" name.


### Day 3: Binary Diagnostic

The second part proved to be much more complex than the first one, more than I
could actually expect; especially, I had .  
Generally, the solution relied a lot on binary to decimal trasnformation, which
actually means "interpret a string as a binary number". I always hated this
kind of exercise, so I was initially a bit scared, but turns out that python --
as often happens -- already got me covered: `int("0100", 2)` will convert a
binary representation.  
It turned out to be very useful, also in other days.


### Day 4: Giant Squid

Approaching this one, I feared about time complexities. The naive solution is
clearly a O(n2), so it was easy to have a second part exploting that fact.  
Still, I decided to go for it; the reason was more to have a way to clarify the
requirements, since it was a bit complex (especially when waking up at 6am!).  
And, actually I was lucky, because second part was just a slight complication.  
Extra bonus fun was then refactoring the code, to remove the duplication between
the two solutions -- I liked, because the refactored approach separates quite
neatly the various concerns: playing game and what to do in case of victory.


### Day 5: Hydrothermal Venture

A simple one; however, it took me quite a lot of time, because of stupid
mistakes while marking the vents -- like counting diagonals incorrectly, and
similar. I liked that the second part was clearly a minor addition on the code
written for the first part and there was no need for further refactoring after
completing the exercise.

As a side note, it's clear that I need to improve my knowledge of regular
expressions. Whenever there is some parsing, I am always a bit afraid to use
regexp, even if the input is guaranteed to be in a certain fixed format.  
Of course, I do know them, and I am quite fluent; but I am not confident
enough to use them as much as I would like.


### Day 6: Lanternfish

This was quick -- less than half an hour to finish.  
Once I decided to use Counter and parse the input data using it, everything
else  was quite straightforward.  
Also, the second part was almost a noop; most probably, had I used a different
approach, it would have caused an explosion in complexity; however, here, it
was just a matter of changing one constant.

### Day 7: The Treachery of Whales

Another quick one.  
It was clearly an optimization problem; for a reason I did not fully analyze,
the first part involved just calculating the median; so after a while, I just
tried, and it worked.  
The second part instead required using some weighted average; at first, I was
again thinking about some general approach, then I tried to just brute force
it and calculate all possible solutions. Turned out it was quick enough, so I
did not try further for a better solution -- which I know exists, but I am not
sure it's a field I want to investigate.


### Day 8: Seven Segment Search

This one took me quite a long time to understand. For the first part, I decided
to use some shortcut -- as suggested in the text, on the other hand -- so it was
relatively simple to do, just some effort in parsing the data.  
However, the second part required understanding the full description, and it
took me a lot of time. To be honest, this was the kind of exercise I dread the
most; on the other hand, this is also a good exercise for daily job.  
Anyhow, this was the first exercise requiring some whiteboard analysis. The
final solution was essentially brute-forced; but it was fast enough, and the
code is actually quite nice -- albeit a bit too terse, and for this reason, in
need of some documentation.


### Day 9: Smoke Basin

Here, I had immediately an idea -- I should use NetworkX.  
NetworkX is a wonderful python library for working with graphs, and it has
already served me several times during advent of code.  
Unfortunately, I seldom use it; as a matter of facts, only during AoC.  
And this is unfortunate, both because I am in love with this library and I would
really love to use it in my daily job, and because I completely forgot about its
usage.  

For this reason, I decided that the first part of the problem was simple enough
to solve it directly using a dictionary; but the second one (recognize the
largest trees in a forest) I felt that it was _screaming_ to be solved using a
better graph representation.

So, I had to read quite a bit of the documentation (and of my previous usages in
old AoC code) to make it working; still I had to somehow implement a function to
recognize the largest trees in a forest, which I am pretty sure **is** available
somewhere in there.  
That said, I am happy to have used it, since it allowed me to model the problem
in a cleaner way.

Some day, I have to write a post about basic NetworkX usage :)


### Day 10: Syntax Scoring

A typical AoC puzzle.  
The solution was pretty simple, you just have to maintain a stack.  
Also, the second part was very similar to the first one, allowing to 
immediately reuse the code there, with just a different rule to calculate the
result.


### Day 11: Dumbo Octopus

This one tricked me!  
Today's exercise is a clear variation on the game of life; as such, I thought it
would have had the classical two-step approach, where the first step is
relatively simple, and then the second step would require some optimization
technique to escape from the algorithmic complexity.  
So, during implementation, several times I stopped thinking about a possible
better approach, then postponing it for a second iteration.  
And then... the second iteration never arrived. I just had to try, and actually
the pattern converged quickly enough to a solution.  
It was definitely one of the most anticlimactic exercises I have done in AoC :)


### Day 12: Passage Pathing

Graph, paths: I immediately thought (again) at NetworkX. However, it looks like
there's no such functionality in there; I spent quite some time searching for
it, but with no result. So I had to implement on my own -- just your typical
depth-first traversal algorithm.  
I still used NetworkX to represent the graph; however, navigate through it was
non-trivial, and required some learning, and the documentation was not clear
for me. Again, I think that I need to write about it, so that next time I will
remember how to use it. In particular, in NetworkX, a graph is a
dictionary-like  structure, where for each node you get the list (sequence,
actually) of all neighbours.

The second part was just a small variation of the first, and came out very
quickly. I just did a copy-paste of the code, and then refactored in a second
moment.


### Day 13: Transparent Origami

Another nice puzzle. For the second part, I cheated a bit, and skipped the OCR
phase, instead transcribing the result manually. Thanks to that, the second
part took me just few seconds.  
However, a quick ddg search revealed a package doing exactly that: 
`advent_of_code_ocr` -- which as the name implies, was created exactly for AoC.
And it worked just fine, allowing to improve the code. A nice tool to add for
next year's AoC, and kudos to @bsoka for sharing it!

### Day 14: Extended Polymerization

This was the first day requiring some extensive amount of time.  
The first part was relatively simple, but it was also clear how the complexity
would have been increased.  
Anyhow, I tried the naive approach -- few days before, it worked anyway. This
time, no luck.  
Eventually, I went for a completely different path -- even _parsing_ data in
a different way, representing data differently: no longer as a string, but as
a counter with all existing tuplets.

The naive implementation was just iterating over the string, splitting into
tuplets, and inserting the correct new letter. With all my efforts, the memory
complexity of this solution was simply too high, so eventually I had to give
up.

Eventually, a new approach dawned on me: we are only interested in counting the
possible pairs ("elements"), and we are not really interested  in their order.
Also, there is a limited number of possible pairs.  
So we can just take the single instance of the pair and the number of times it
appears; and then we can just move on from there.  
I like this new solution quite a lot; the only problem is that the code is not
very readable, but with such weird requirements, it's difficult to make some
sense in it.


### Day 15: Chiton

Another one solved using NetworkX. It was clearly a Dijkstra exercise on a
directed graph, where the weight of the edge was the "risk level" of the target
node.  
The second part would have been straightforward... if it weren't for some silly
bug I introduced; and when it was taking too much time, I wrongly interpreted
it and tried to analyze performance, instead of functionality.  
That said, it was a nice exercise, and again, NetworkX was a huge help.


### Day 16: Packet Decoder

This is not really my favourite type of exercise; it's essentially an exercise
in parsing data according to a specification. And there are always some small
items in the specification (in this case the padding) that are somewhat obscure
and you have to guess, and try to fill with your interpretation.  
I always felt weaker in this kind of exercise. I still remember reading the 
[BMP file format specification][2], and feeling a sense of panic at it. Well,
here it took me quite some time to do, but eventually I did it; moreover, the
approach was good enough to quickly manage the second part as well, with almost
no additional code required.


### Day 17: Trick Shot

A quick one. It is a clear homage to the old theme of the [artillery games][3],
of which I remember especially my experience with _Scorched Earth_.  
Also, it reminded me an evening, spent coding with friends in a kind of code
competition, writing some AI to play the artillery game against each other. We
lost, and by good margin, but it was fun.

As usual in this AoC, I tried the naive solution, knowing it was for sure good
enough for the first part, and at worst, could give some good hint for the
second part. Actually, the approach was fast enough to be used even for the
second part; eventually, I optimized it with a smaller range to search for all
trajectories, so that it could always run in the runner. I could optimize it
automatically, but I was happy it could be finished in few minutes, so I did
not investigate further.


### Day 18: Snailfish
This was one of the hardest, like the fourth hardest, and required a lot of
time to solve; fortunately, the second part was just a small increase in
complication.  
For some reason, the "explode phase" failed my attacks for long; my final
approach, while working, still looks way too complex. I am pretty sure there
is a simpler and better approach, most probably modeling data in a different
way.

This is the first time when I had to write a fairly amount of test cases; and
it was good that there was enough examples to create them. I was tempted to
add pytest to the project, but eventually let them as simple ad-hoc functions.


### Day 19: Beacon Scanner

Another tough one, at least for me. This is one of the areas where I know I am
weaker; and all the rotation matrixes were quite difficult to derive and use.  
Maybe, if I had added numpy as dependency, I could have done it much faster;
but I did not want to learn it now. Also, the solution is clearly suboptimal,
as it's way too slow. But hey, it works :)


### Day 20: Trench Map

A relatively easy one. The pattern here is a common one, à la Conwayàs game of
life: create a function calculating the next iteration of the "map", and then
if necessary discard the previous one. In this case, the algorithm was actually
quite slow; fortunately, it was not so slow to require improvements or rework.


### Day 21: Dirac Dice

Again, it was clear that the first part was just an introduction for a second
part with an impossible algorithmic complexity. And that happened.  
I worked quite long to make it work, but with no success. Then I tried to just
cache it, and much to my surprise, it simply worked.
For the cache, I leveraged the excellent `functools.cache` decorator: just one
line of code, and I got a simply working memoization.


### Day 22: Reactor Reboot

We are now entering the last phase, with exercises that were **much** harder,
and I had to systematically interrupt in order to do other stuff. Like, work,
or Christmas -- sometimes I wonder why people expect those to be more important
than AoC.

In this case, the second part required a completely different approach than
the first one. Finding it required quite a lot of whiteboard work (where I
simplified the problem to a 2d representation), but it was eventually a
satisfying experience. Tiresome, but satisfying.  
I have then refactored the code, using only the new approach also for the first
part; with the new approach, it turned out that the first part is slightly more
complex than the second :)


### Day 23: Amphipod

This was one of the most challenging, but at the same time my favourite.  

The solution was clearly a matter of finiding the shortest path on a graph;
however, defining the graph and the weight was not a trivial task. Defining all
possible states was out of question, because of the sheer number; and then, I
was struggling on a good definition.

The general idea was simple: this is a graph, where the start is the initial
state, and the end is the desired state.
Then, we just need to use something like A* to go from one state to another; we
need to  generate available states (movements) and costs.  
In particular, we need to:
 - Represent the state in a good structure
 - Implement the "move"
 - Implement the pathfinding algorithm

Initially, I wanted to use NetworkX, but then, defining the graph dynamically
would have required some non-trivial work with generators and memoization;
eventually, I simply started to implement the Djikstra algorithm (which, using
python's [heapq][4] become a trivial matter) and create the state and its cost
on the fly. The algorithm is a tad slow -- and unfortunately that slowness hid
some bugs that took me quite a lot to find -- but it works in a reasonable
amount of time.  

And that was an issue, because I did not implement all requirements!  
In the short version it worked fine, but it took a lot of debugging (and time!)
to  understand that the longer version was no longer working!

Definitely my favourite exercise, and solution, for this year's AoC.


### Day 24: Arithmetic Logic Unit

I knew this was the last day with a complex exercise; and actually it was maybe
the most complicated one.  
Also, it was a weird one, with little or no test data, and that had a
"mathematical" solution. I tried to explore using a solver like S3, but it was
definitely out of question in such short timespan.
Eventually, my implementation _was_ correct; and again, it was just had some
trivial bug preventing it to find a solution. Once fixed the bug, it started
converging reasonably fast -- even if it's still a "slow" one -- by far the
slowest of the bunch.  
Note that there **are** better approach, and I checked a couple of them; they
find a solution much faster than my approach. Still, I am not sure that I
completely understand them, as they use some relationship within data that
somehow require a different kind of analysis.

Overall, not really my favourite exercise; the fact that I had to finish it
using breaks during Christmas dinner did not help. That said, I have to admit
that the "decompiler" part was indeed quite fun.


### Day 25: Sea Cucumber

For the last day, as usual we have only one part, with the second just checking
that the all the previous ones have been completed. It was also quite an easy
one, with yet again the same kind of pattern as in day 20, with the additional
complexity that now each iteration is actually split in two parts with
different rules.

And with this, even this AoC has been completed.  
Overall, a better experience than last year, and one of my favourite -- not too
demanding, and more on the "fun" side.  

Main take-aways for this year:
- Become more fluent using regular expressions.
- Better at linear algebra. Not sure if it will have an impact on anything else 
  than AoC, but I always felt that as something I forgot too fast.
- [heapq][4] is an underrated module in standard library.
- NetworkX is cool, and I need to becoem a bit more proficient with it.

I am looking forward for next year!


[1]: https://docs.python.org/3.8/library/collections.html#deque-recipes
[2]: https://docs.fileformat.com/image/bmp/
[3]: https://en.wikipedia.org/wiki/Artillery_game
[4]: https://docs.python.org/3/library/heapq.html