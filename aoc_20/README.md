## Day 1: Report Repair

I actually forgot about AoC, this year, so I started it late.

So, today's task was quite a typical interview coding task, with just some story
about Christmas (small OT: I really hope we are going to save Santa again!).  
This was one I was fully prepared, having done it countless times; but I suspect
that the second part, without an efficient first part, could have taken a bit
too much time.


## Day 2: Password Philosophy

Again, a simple one. We are just in the early phases of the game :)
I am not very happy with the solution, but it worked at the first try.

This time I am using less ipython, and more python with type hinting. I am not
sure if this is not removing the fun of the thing, or it's just that I got used
to it. But I also appreciate taking it a bit slower, and going in a simpler
and steadier way.


## Day 3: Toboggan Trajectory

And we start with maps :-)

With the experience of previous years, it was not a difficult task. The final
solution is smaller than the previous day, even if it required a bit more
programming.  
However, it took me a bit too much time than I was expecting. Eventually, I had
to debug to discover a silly off-by-one mistake. I suspect the decision to wake
up earlier to work on the problem had an impact on my performance :-)  

I like having decided to use a generator for representing the function. It made
the solution much nicer to see, and the second part almost a breeze.  
Also, I have learnt a nice new corner of python 3.8: `math.prod`.


## Day 4: Passport Processing

This time, I used pydantic a lot.  
The entire exercise here was about data validation, and this is an area where
pydantic really shy.  
Actually, I started with simple dataclasses, but soon the lack of validation
there led me to the full pydantic.  
A small problem blocked me for long -- I had to solve the first exercise in a
different way, just to debug it: as a legacy from using dataclass, I was still
assigning `str(value)` to a non-nullable  string field; and that was enough to
skip the validation. The field was `None`, but for some reason that was not
detected.

Overall, an easy one -- but I could have done much quicker if I had used
pydantic from the beginning, and strictly followed its approach.


## Day 5: Binary Boarding

This one was an easy one, once you realized this was a binary number.
Just convert the string into a string of 0 and 1, and then let the built-in
take care of its conversion.

Too bad I woke up late this time, or I could have had my personal record :)


## Day 6: Custom Customs

Again an easy one, and again I woke up late :)

Also, this time I over-engineered the first part, expecting something more from
the second.  
Often, the wrong abstraction (or the lack of thereof) on the first part lead to
a much bigger effort on the second. Like usual, in in software maintenance, btw.
That means that one of the challenges in the first part is usually to try
guessing what the second could be.  
In this case, I was expecting some very different kind of logic; so I introduced
an intermediate "Form" class to hold the single answer and to which delegate the
calculations. However, already during implementation, it turned out to be just a
holder of a string, so this class was removed in the final clean-up. Overall, it
did not waste too much time; however, not wasting time at all is also one of the
challenges of AoC.

In this case, the solution used extensively python sets, and the fact that a
string is an iterable. With those two concepts, the solution is actually quite
trivial.  
Note that this is already the second time that I have to use a "buffered lines"
parsing.  
This was a hint to refactor it to a common function, which actually helped to 
clean the code in both places.


## Day 7: Handy Haversacks

This time, we started with trees.  
The first part was essentially the number of (sub) trees containing a specific
leaf, while the second a normal traversal.

For the first, I decided to use a shortcut, and just check the string itself.  
This had the main advantage of not forcing to parse the second half of the
rule. I was pretty sure that the second part of the exercise would have asked to
do that, but after yesterday's experience decided to go for the easiest approach
also because it would not have caused any additional "debt".

This approach also had the advantage of validating the second part: by swapping
the second half implementation, from a string to a dictionary, I was able to
quickly validate the parsing. As a side effect, the second approach was
noticeably faster -- this is not something I expected, being all short strings.


## Day 8: Handheld Halting

It seems quite a tradition now, the VM-based puzzles, and this year is no
exception.  
For this reason, I took some time to clean-up the code after finishing,
refactoring in a way that _might_ make the VM hopefully more open to changes.

Maybe I should start implementing some enhancements _before_ the next puzzle,
in order to be ready with it. For instance, memory management, more registers,
and indirect store/load.

Except for that, the puzzle was fairly straightforward. The simplification for
finding the infinite loop (just go again on the same instruction, no matter the
state) was really nice, because otherwise it would have been a much more complex
problem to solve.


## Day 9: Encoding Error

This one was a bit... disappointing.  
The first part was OK. I did not try to brute force it, but it still _looks_
like maintaining a round robin of pre-calculated values was the correct choice.  
The problem is with the second part: it looked scary, so I tried to analyze the
data, but with no luck. Eventually, I tried to brute-force it and it worked,
with the most naive solution possible.

Sometimes, the most naive solutions are good enough. Maybe that's the learning
for today.


## Day 10: Adapter Array

Again a short puzzle, but this time a satisfying one.  
- First part was solvable using only python batteries (plus pairwise itertool
  recipe): sorted, pairwise, counter.
- Second part was solvable again using python batteries and a dynamic
  programming approach.  
  Note that without memoization the solution would have taken ages; this is
  something even the description was hinting at.

This is the first time I am using `functools.cached`, and I was in for a couple
of surprises:
- `cached` is available since 3.9 (I am still using 3.8), even if it's already
  in 3.8 libs. Prior version can use the slightly more expensive alternative,
  `functools.lru_cache`, with `maxsize=None` and have the same effect.
- It is not possible to specify a key for the cache a nd the _entire_ argument
  tuple is used as a key for the cache.  
  This was something a bit surprising for me, and it forced me to pass a couple
  of (fortunately read-only) parameters as global objects.


## Day 11: Seating System

Today, I am pretty sure I have ended up with a sub-optimal solution.
It takes few seconds to complete -- an _acceptable_ amount of seconds, but still
it is not instant.  
Furthermore, it took much more time to solve than usual, and this is another
hint that I have chosen the wrong data structure.

For part 2, I wanted to treat the map as a graph, and simply connect nodes
skipping the floors. I decided to take the effort to refactor part 1 as well,
because it was still useful as a test case for all the parsing (I do a lot of
small mistakes there), but again, the slowness of the test was annoying.

Overall, it came out almost at the first try; still, I cannot stop thinking that
I could have used a better approach.

#### Update after Day 13

Today, I took the chance to work a bit on the performance.  
The new approach is _much_ faster, but still _slow_. I am afraid this is the
best I can do with pure python. Tha algorithm more or less stayed the same, with
one important optimization (trace only changed seats); maybe there _is_ another
approach much more performant.

Moving from a "pure functional" approach, with immutable data, to changes in
place helped cutting times by half. This is a very data-intensive exercise, so
this was quite expected.  
Then, tracing helped cutting another second and a half, plus a bunch of other 
small changes (including using `__slots__`, which helped gaining about 200ms) to
arrive to a final execution time a bit lower than a couple of seconds.  
Maybe using something like [Nuitka](https://nuitka.net/) might help, but it is
already taking a bit too much time...


## Day 12: Rain Risk

This was instructive!

I always have issues with rotations. I know the basics, I know the general
ideas, but when I need to start doing it, I feel like trigonometry was too far
in the past, and I am not able to do anything.  
So I usually navigate my way through, trying to reinvent the math.

This time, I wanted to sit down, and find a better answer.
First refactoring, was to use a matrix for the rotation. A point is a vector,
and can be rotated my multiplying with a rotation matrix.  In our case, the
rotation matrices are very simple, as we only rotate by 90  degrees:
`[[0, -1][1, 0]]` and so on.  
This first approach was very nice, and reduced the bunch of `if`s quite a lot;
still, the code, using tuples for the coordinates was too complex.  
So I realized that a point is a complex number; and then, in a complex number,
we can easily extract the _phi_, and make sums like champs thanks to `cmath`.
There is some additional issue now, related to integers: AoC uses integers only,
but `complex` are float, so there is now the need for rounding, and the risk of
floating point errors.  
Anyhow, the new approach was even simpler, but it still was wasting too much
branches  for the translations over x and y.  
The last approach (almost) unifies all movements across all axis (x, y, rotate),
with a much simpler dispatching.  
It's not perfect yet, but I think it's enough for the moment.

Learning items:
- Linear algebra -- this is something I need to study again
- `complex` and `cmath` in python -- they are really nice!


## Day 13: Shuttle Search

Oh, back to algebra!  
There was a time, when I was quite proud of my algebra skills. Unfortunately,
that was a long time ago, and I guess this is what happen when you do not
exercise :-)

Anyhow, the problem was interesting. In part 2 I immediately realized this was a
set of equations in modulo, but I had no idea on the strategy to solve them; so
I had to setup my own strategy.  
In this case, the strategy involved solving the equations one by one, and then
increasing the modulo.  
Once I find a time `t1` solving an equation in modulo `m1`, then any solution
for  a second equation in `m2` must also satisfy the condition `t2 == t1 (m1)`.
And since `m1` and `m2` are prime (I did not check, but it looked so), then the
solution must satisfy both conditions in modulo `m1*m2`.  
From there, the implementation was quite straightforward, but not so much -- I
was able to put few bugs here and there, that required some time to be ironed
out.  
For instance, the actual input had an interesting difference from the sample
one: in the sample, all periods were higher than the desired time, while in the
actual input there were a couple of buses with period smaller than the desired
time. Obviously, I had a bug in my code, and I spent quite some time scratching
my head thinking why it worked in one case, but in the other not :)


## Day 14: Docking Data

OK, this was a kind of typical problem. A nice one, but not one of the best of
this year.

Part 1 was quite straightforward, but I have approached it in a bit too messy
approach. I had some issues in making up for the correct data structure. It
turned out that this time the data structure was almost non-existent, just a
series of commands, and nothing to think about that. Maybe that's the reason why
I could not grasp it initially.  
Small piece I particularly like in this solution: the transformation of a
"partial" mask to two "logical gates".

Part 2 got me quite in panic. Reading the description, I started to expect
instructions affecting a huge amount of memory addresses, and then I started to
think hard about how to cope with that. I spent quite some time trying to figure
out patterns for discerning the latest change to an address to discard all the
previouses; but then I realized that that was not happening, that each mask was
affecting just few addresses, and that and that a simple list was more than
enough to manage it. Then, everything else was just flowing.

Interestingly, it took a bit more time than usual to cleanup the code, after
writing; either I am becoming more and more picky, either this time the lack of
a strong structure for the data was making things more difficult.


## Day 15: Rambunctious Recitation

It took my quite a while to parse the instructions. I know that in these cases I
make quite a few mistakes, so I wanted to be extra cautious.  
In the end, the code was quite simple. In a different language, I would have
used recursion, but this would have hit python's limit before reaching the
result, so I went with an iterative approach.

Then I went to part 2. It looked like my code was able to do it without any
special modification so I tried it.  
And then I stopped after about 20 seconds, thinking that it was wrong, and that
it needed some special optimization. So I started to trace the output, trying to
find cycles, but with no luck.  
Eventually, I put a progress bar -- to discover that yes, it was slow, but it
_was_ going to give a solution, if only I were to wait a bit more.  

After that, I tried to optimize the code.  
The initial approach was taking a bit more than a minute, but it was maintaining
a list with all the occurrences, while we needed only the last two.  
So I swapped that with a tuple, and processing time went considerably down.  
I was aslso able to shave a bit more time, down to about 26 seconds, using some
of the usual tricks, like caching dictionary lookups.  
One of the most interesting finding was that, according to profiler, most of the
time now is spent in _subtracting two integers_ (`PyNumber_Subtract`). Now, I
remember watching a presentation, about the costs of simple operations like
additions, and that the support for seamless switching to infinite precision
increased that cost even more; but I find it a bit disappointing that we cannot
"hint" that this is a small number, and that elementary operations could be done
in a much more efficient way. Maybe the assumption is that in such cases you
would directly use numpy?

Another round of optimization, this time with subsequent algorithm refactoring,
brought to another nice speed increase.  
The idea was to get rid of the tuple maintaining the two last times the number
was spoken. Doing so, allowed getting rid of quite a few checks, for cases that
were not happening any longer. Also, getting rid of the tuple allowed to reduce
the number of object allocated, giving a good improvement as well.  
Now, the time is down to approximately 10s, and again, the "hot path" is either
on the increment operator (when using `while` loop) or in the for declaration.


## Day 16: Ticket Translation

This was sa smaller one.  
It looked complicated, but most of the work was actually parsing the data and 
(mis)understanding requirements. So, almost normal daily job :-)  
The first part was easy to translate to something nicer using `reduce`, but the
second part still looks like a bunch of nested loops. That said, it does not
really entice me in further analyses, like instead yesterday's puzzle.


## Day 17: Conway Cubes

This type of puzzle (or at least a variant of it) is a staple in AoC. My initial
assumption was to optimize for performance with large sets; but then I decided
"oh, screw it and let’s see if really part two will have thousands of
iterations". From there, implementation was simple; and actually that was a good
choice, because extending for part two was quite simple, and performance was not
a problem (around two seconds).
After a couple of optimizations, I was able to get in the below-second ballpark.
Interestingly, the bulk optimization was to remove memoization, and instead use
a  generator (instead of small list) with an early exit in the loop using it.
Another optimization, made the code uglier -- but it was able to make it much
faster (around a quarter of second) so I had to leave it. The previous solution
was iterating over node neighbours twice: the first time to get all the
candidates for being acttive, and then to get all their neighbours. However,
this can be merged into one single (nested!) loop, recreating the graph. Not
nice, but works better -- as often with performance optimizations.


### John Horton Conway (1937-2020)
I remember first implementing game of life in Turbo Pascal. I should still have
that code, somewhere; I am pretty sure it would make me frown for its ugliness.  
But I remember watching those patterns, moving around the screen, and hitting
performance limits (I did not know about complexity at the time) of my computer
when I wanted to make a version that could fully exploit the incredibly high
resolution of my graphic card.  
All of that, was out of an article I read on an old "Scientific American" found
in my father's collection.  
Since then, I reimplemented it countless times; for my pleasure, in interviews,
in AoC (at least in some variant). And it was always fun.  
This time, however, it was a bit sad.  
[RIP, Conway](https://www.scottaaronson.com/blog/?p=4732) 


## Day 18: Operation Order

I am not really satisfied with this one.  
I felt panic when reading the description, and for the first time I attacked the
problem with a "code-first" approach. Which paid off in the first phase (I got
my first placement under 1000), but made the second part much harder to solve.  
Eventually I cleaned up the code, and had it a bit nicer; still I am not fond of
this approach: what is the _purpose_ opf those classes? What is the _advantage_
of this approach against a regular expression approach, removing iteratively all
"inner" tokens, replacing with the result?  
The current approach has the advantage that I can represent the expression. Is
that enough of a vantage?

As usual, every year AoC exposes some part in my baggage that I need to improve.  
This is definitely one of those case.


## Day 19: Monster Messages

This one was fun.  
This was all about regular expression; so it would only make sense to leverage
existing `re` module.  
As usual, the parsing was the slowest part for me. I realize more and more that
I am really inefficient at parsing the problems; and that I should rely more on
regular expressions for that.

I panicked when reading about part 2. It was clearly not something that I could
describe with regular expressions, so I started to think how to roll out my own
simplified matcher, while being really upset that I had to reengineer the
solution again.  
Then I realized that all I had to do was breaking the recursion, and then it was
definitely easy -- and this was also the first time my second part was in the
top thousand.

Overall, another fun puzzle :)


## Day 20: Jurassic Jigsaw

OK, this was a marathon.  
I spent a _huge_ amount of time on it: to get it, then to make it faster, and
finally to make it better.

My initial assumption was to solve everything in one go: find the connected
pieces, and rotate/flip them in the correct position.  
That was wrong. Eventually, I got it working, but it took a huge amount of time,
and the algorithm was very slow. Not only: since positioning on the first part
was not reliable, I had to introduce a "fixing" phase -- but it was all just by
accretion, and not really maintenable.

Interestingly enough, once I had a working solution, I realized a much better
approach. It was simpler to implement, with less code, less debugging, and less
time.  
In this new approach, I follow two steps: first, connect the pieces, and then
flip/rotate them. Essentially, very similar to what was done before, but
explicit. This led to various simplifications (especially in the first part),
and a substantial increase in readability and performance.

More in detail, the first parts have two moments:
- Connect all tiles
- Corners are the only tiles with two neighbours

As well, the second part:
The idea for the second part:
- Generate the image starting from the corner 
- The corner must be aligned so that it's top-right
- Move in a "serpentine" pattern and rotate/flip each tile so that it fits the
  previous one and the one above (it looks like we need two tiles to block all
  degrees of freedom)
- Use set inclusion to check the dragon presence (the set of the tranlsate
  dragon dots must be contained in the hash dots)

I have still an unknown: why do I have to rotate/flip the first tile, to be in
that position? If I do not do that, I get a map that looks valid, but does not
yield results. I suspect I had some bug in determining the direction for
scrolling the map; anyhow, the current approach (fixed directions) seems to
bypass that issue, without side effects.

Anyways, I have already spent enough some time to refine the code and improve
its quality. I am not 100% satisfied with the code as it is now, and its
unknowns; however, it is also important to set a limit -- it works for my input,
it _seems_ be already readable enough, so be it.


## Day 21: Allergen Assessment

This is my least favorite type of puzzle in AoC:
- Not really much challenging
- Most of the effort is in understanding the requirement (without possibility
  to ask for clarifications)

In my case, I spent quite a lot of time trying to understand what the problem
statement was; and then, I was going very cautiously to get the things right,
since I was not sure about the problem and the strategy to use.

Worth mentioning, it was maybe one of the first times I have seen a string
output in AoC. I had to rework the general runner because of this :)


## Day 22: Crab Combat

Again, one puzzle where most of the effort was in understanding the problem
statement. And this time, I spent a **lot** of time because I missed one detail,
and then it appeared only after re-reading several times.  
That detail was key in making the second part converging, whereas I spent a lot
of time trying to cut down on the execution times. I knew that the algorithm was
wrong, because execution times are always short, but I thought I had to find
some clever optimization. And instead, it worked from the beginning, it just had
to pass the correct data.

Nothing really to comment on the implementation; I am not really a fan of it and
it is a tad too slow; but after spending some time trying to make it faster and
easier to understand, I decided to stop and move over. It's anyways interesting,
because in the end the same algorithm (with one small flag) was able to perform
both parts of the problem.
