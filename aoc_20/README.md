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
