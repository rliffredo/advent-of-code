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
