Please generate a metamodel of a simple library management system with three main concepts: Library, Book, and Author.

Each Library has a name (String) and contains a collection of Books and a collection of Authors (both containment references).
Each Book has a title (String) and a page count(int) and has a non-containment reference to its main Author.
Each Author has a name (String) and age (int) and knows which Books they have written (non-containment reference to Books).

The system should clearly distinguish between containment and non-containment relationships:
- A Library owns its Books and its Authors (deleting the Library deletes its Books and its Authors).
- Authors and Books reference each other but do not manage each other's lifecycles.
