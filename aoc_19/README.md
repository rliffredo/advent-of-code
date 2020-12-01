## Day 01 - The Tyranny of the Rocket Equation

For being the first task in AOC, it looks definitely more difficult than other
years. Last year, you could solve the first couple of tasks easily with just
a calculator, while here you need a small algorithm.  
The additional fuel part was a very nice reminder to the rocket equation and
its tyranny (as the puzzle title implies).


## Day 02 - 1202 Program Alarm

OK, we have again a VM. Last year taught that such a VM might be reused few
times, so I wanted to have it well done.  
The result was quite good, as it went through all the changes of subsequent days
without any bigger design change.  
That said, I had quite a lot of issues in making the correct abstraction for the
memory indirection. For some reason, I could not get it right initially, and it
took me quite a long time to fix the bugs.

## Day 03


## Day 04


## Day 05


## Day 06


## Day 07 - Amplification Circuit

I was initially happy that my IntCode VM design was perfectly capable for this
task.  
And then I started coding :)

I really wanted to go with async -- essentially build a state machine with each
amplifier asynchronously pulling from the previous one, until we get to the
initial input state.  
Unfortunately, it did not work. I could not make it so that each amplifier is
asynchronous in the input _and_ the output.
Eventually, I got quickly to the solution using threads; but I am not
satisfied.

I need to get better at python async; I also believe that a simple framework
of loosely coupled "objects" exchanging data asynchronously and chatting with
each other might be a very good tool.  
I wonder if it already exists.


## Day 08


## Day 09


## Day 10


## Day 11


## Day 12


## Day 13


## Day 14


## Day 15


## Day 16 - Flawed Frequency Transmission


## Day 17 - Set and Forget


## Day 18 - Many-Worlds Interpretation

One of the most difficult. I approached the problem with a DFS algorithm
(essentially because I love recursion when traversing graphs) but it was not
efficient. Switching to a BFS approach ensured a quick solution of the
problem... with the exception that I used the wrong distance function.  
Debugging it took very long, and it was actually just by chance that I found
what the problem was.

Next time, I think that in such cases I should go back to the drawing board
and check the ideas and the assumptions.

The final version took me quite a lot of time, and I am not really satisfied
with it. Clearly, ot took too much time, hence it must be too complex, and
a smaller and better version must be available. That said, it works and is
also a bit more generic than required, as it does not exploit that the map is
split into four quadrants.


## Day 19 - Tractor Beam

Solution for part 1 was quite straightforward -- just throw in the standard
IntCode and collect the output.

The second part was (quite as usual) raising the size of the input, so that
the "easy" approach would just take too much time.  
In this, I had finally the chance to re-use the snapshotting feature
introduced very early in the IntCode VM, and almost never used; and thanks to
this, I was able to reach a solution much faster.  
The generic approach was:
- Observe the shape of the beam (it's essentially a V rotated) and get the
  approximate parameters
- Move along that axis, until a good candidate to be the top-left corner of a
  100-side square is found.
- Move back alternatively one direction and the other, until we find the best
  solution


## Day 20 - Donut Maze

Most of the effort of the task was about parsing the input data -- teleports
were a slightly different concept than usual.  
Everything else, just the usual graph traversal.


## Day 21 - Springdroid Adventure

I made the mistake of spending time creating a "SpringVM", which was totally
useless. When I switched to creating a script, to feed the IntCode, it went
quite straightforward.
The input was not really clear: the jump is always 4 lengths long, and it
always land on the D tile.
After that, a bit of analysis of the map, and a lot of DeMorgan, and the
solution came much faster than expected.


## Day 22 - Slam Shuffle

Algebra!
This has been the hardest problem for me, with second part still without an
original solution.


## Day 23 - Category Six

This time, it was quite straightforward.  
Except that it wasn't, but for my fault :)
1. I did not read correctly the requirement.  
   Because of this, the intocode program was crashing; unfortunately,
   instead of reading _better_ the requirement, I started analyzing the IntCode
   VM to find issues.
2. IntCode VM was not working correctly in multithreading. Here, the reason is
   subtle: among the performance optimizations, I compiled it using nakata.
   This worked very well so far, but once it moved to multithreaded, it simply
   stopped working reliably. Most probably, some guarantees are not respected
   any longer -- I did not investigate throughly. Switching it off, made it
   working again, but if it were not for my first mistake above, it could have
   taken much more time.


## Day 24 - Planet of Discord

Again, a fun exercise.  
A variation on Conway's game of life, with a "recursive" rule.

I tried some different approach than usual for data structure (a single
string), but I am not sure that it was the best choice. It was quite fun,
though :)

The major blocker, here, was the "mental visualization" of the problem.  
Until I did not go on the whiteboard, to write it down, and write down all the
connections, I could not visualize the problem, leading to a series of small
bugs, slowing down.

Lack of explicit test was also not helping. It would be good to have some unit
testing, but that might slow down too much for the AOC purposes.


# Day 25

This was weird :)

The input was quite vague, so the first step was to just "run the intcode
program" and look at the result.  
Then, it was obvious that a manual exploratin could have been a fast approach,
as the map can't be huge (intcode program was big, but not that big) and
parsing could proof expensive.  

The puzzle, however, was easier to solve just by brute force and try all
combinations. I spent some time trying to solve it manually, but that was a
waste.

As usual, the second step was just formal.  
Overall, a nice puzzle, completely different from the others, because of the
mixed approach.  
Fun :)
