## Metadata
- **Date:** 23-05-2026
- **Source:** 04_data_strcutures.txt
- **Model:** claude-opus-4.7
- **Prompt:** cognitive-assets/prompts/competencies_db_level_1_post.txt

## LLM Processed Content

# Data Structures

Most performance problems in production code are not algorithm problems. They are data structure problems wearing algorithm costumes. A loop that scans a list to find an item is not slow because the loop is badly written; it is slow because a list is the wrong place to look something up. The choice of where to put data — and the shape of the container you put it in — quietly determines what your code can and cannot do efficiently. This is the layer where most real engineering decisions about performance actually live, even when the discussion above it is framed in terms of algorithms.

The clearest way to understand data structures is to see them as a sequence of inventions, each one designed to fix a specific limitation of the one before it. The history is not just chronological trivia; it is the actual logic of why the field looks the way it does. You do not need an array, then a linked list, then a hash table because someone decided variety was nice. You need each one because the previous one had a concrete weakness that mattered enough to design around.

Start with the array, because every other structure is in some sense a response to it. An array is a contiguous block of memory holding elements of the same type. Because the elements sit next to each other, you can compute the address of the nth element directly — there is no searching, just arithmetic. This gives you constant-time access by index, which is the fastest possible lookup. The price is rigidity: the block is fixed in size, and inserting an element in the middle means shifting everything after it. Arrays are fast where they are fast and slow where they are slow, and almost every other structure exists to trade some of that speed for more flexibility somewhere else.

The linked list is the first such trade. Instead of placing elements next to each other in memory, you scatter them and have each one point to the next. Insertion becomes cheap — you just rewire two pointers — but lookup becomes expensive, because to find the nth element you have to walk the chain. Stacks and queues are then conventions layered on top: a stack restricts you to adding and removing from one end (last in, first out), a queue from opposite ends (first in, first out). These constraints sound limiting until you realise that almost every act of parsing, every function call, every undo system, every event scheduler is naturally one of these two patterns. The structures are simple; their ubiquity is what is striking.

Hash tables are the answer to a different question: what if you do not want to look something up by position at all, but by name? A hash table takes a key, runs it through a function that produces an index, and stores the value at that index in an underlying array. The result is near-constant-time lookup by arbitrary key — the foundation of dictionaries, caches, database indexes, symbol tables, and roughly half the data-handling code you have ever written. The qualifier "near" is doing real work, though. Two keys can hash to the same index, and how you handle that collision — and how full you let the underlying array become before resizing — is where the performance story actually lives.

Trees take a different approach again. Instead of one element pointing to the next, each element points to several children, forming a hierarchy. This is the natural shape of file systems, the DOM, parsed source code, and many database indexes. The reason trees matter for performance is that a balanced binary search tree turns lookup into a process of repeatedly halving the search space — logarithmic time rather than linear. Heaps are a specialised tree with a single useful property: the smallest (or largest) element is always at the root, retrievable in constant time. That property is exactly what a priority queue needs, which is why heaps sit underneath schedulers, event loops, and efficient sorting algorithms like heapsort.

Graphs are the general case. A tree is just a graph with constraints — no cycles, one path between any two nodes. Drop those constraints and you have the structure underneath networks, social connections, dependency resolvers, routing systems, and most genuinely interesting real-world problems. A surprising amount of analytical skill in software comes down to recognising that something you thought was a list-of-things or a tree-of-things is actually a graph, and that the right vocabulary for reasoning about it has been developed elsewhere.

What unifies all of this is the idea of a tradeoff space. There is no universally best data structure, only structures that are good at certain operations and bad at others. Arrays are fast to read by index and slow to insert into. Linked lists are the reverse. Hash tables are fast for keyed lookup and useless for anything ordered. Trees give you ordered traversal at logarithmic cost. Choosing well means knowing which operations your code performs frequently and which it rarely performs at all, and picking the structure whose strengths align with that profile. Choosing poorly is how you end up with code that works fine on small inputs and falls over on large ones.

The skill this topic builds is not memorising operation costs from a table. It is learning to look at a problem and see, underneath the domain language, which abstract structure it actually is — and therefore which costs you have already committed to the moment you reach for the wrong container.

## Level 2 candidates

**Arrays** — How contiguous memory enables constant-time indexed access, and what that contiguity actually costs in allocation, resizing, and insertion. Worth deeper treatment because the array is the substrate most other structures are built on, and understanding cache behaviour at this level explains a great deal of real-world performance.

**Linked lists** — The mechanics of node-and-pointer storage, the tradeoff against arrays, and the historical role of linked lists as a workaround for fixed-size memory. Worth depth because the structure illustrates how memory layout, not just operation count, determines performance — a lesson that recurs everywhere.

**Stacks and queues** — The LIFO and FIFO disciplines and where they appear: parsing, call stacks, scheduling, breadth-first search, undo systems. Worth depth because seeing the same two patterns recur across so many domains is what trains the eye to recognise them in unfamiliar problems.

**Hash tables** — Hash functions, collision resolution strategies, load factors, and rehashing. Worth depth because "near-constant" hides real complexity, and the pathological cases are where production systems actually fail.

**Trees** — Binary trees, balancing, traversal orders, and the logarithmic-time property that makes them indispensable. Worth depth because the family is large (BSTs, B-trees, tries, red-black trees) and each variant exists for a specific reason that is worth understanding directly.

**Heaps** — The heap property, array-backed heap implementation, and the connection to priority queues and heapsort. Worth depth because heaps are the canonical example of a structure whose entire usefulness rests on a single invariant, and that pattern is instructive in itself.

**Graphs** — Representations (adjacency list vs adjacency matrix), the basic vocabulary of nodes and edges, and the recognition skill of seeing graph structure in problems that do not look like graphs. Worth depth because graph thinking is one of the highest-leverage analytical lenses in applied work.

---