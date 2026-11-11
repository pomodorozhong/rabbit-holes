# Why an include guard can't fix a C++ header cycle

**Main finding:** An include guard stops the preprocessor from reading a header twice in one translation unit. It can't supply a declaration the compiler hasn't seen yet, so two headers that need each other still fail. Break the cycle with forward declarations, and move code that needs the full type into a `.cpp` file. [C++ Core Guidelines on cyclic dependencies](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-cycles)

**What does an include guard fix?**

- A **translation unit** is one `.cpp` file plus the header contents the preprocessor inserts into it. Each one is compiled separately.
- Two independent headers may both include a third header that defines a class. Without a guard, that translation unit sees the definition twice and the compiler rejects it. With a guard, the second copy is skipped. [GCC on once-only headers](https://gcc.gnu.org/onlinedocs/cpp/Once-Only-Headers.html)

**Why does a cycle still fail with guards?**

- Suppose a `Report` can ask a `Writer` to print it, and a `Writer` accepts a `Report`. Then `main.cpp` includes `report.hpp`, which includes `writer.hpp`, which tries to include `report.hpp` again.
- The guard skips that second visit, which stops the loop. But `report.hpp` hasn't reached its `Report` declaration yet, so `writer.hpp` mentions a name the compiler doesn't know.
- Reversing the include order only changes which type name is missing.

**How do forward declarations break the cycle?**

- A *forward declaration* such as `class Writer;` says the name is a class without describing it. That's enough for a reference or pointer in a signature.
- The compiler needs the full definition to reserve space for a by-value member or to compile a method call. So those uses move to the `.cpp`, where both headers can be included.

This example has four files in one directory. One header uses a guard and the other uses `#pragma once` only to show both forms; a real project would normally pick one.

`report.hpp`

```cpp
#ifndef REPORT_EXAMPLE_REPORT_HPP
#define REPORT_EXAMPLE_REPORT_HPP

#include <string>

class Writer;

struct Report {
    std::string title;
    void print(Writer& writer) const;
};

#endif
```

`writer.hpp`

```cpp
#pragma once

struct Report;

class Writer {
public:
    void write(const Report& report);
};
```

`report.cpp`

```cpp
#include "report.hpp"
#include "writer.hpp"
#include <iostream>

void Report::print(Writer& writer) const {
    writer.write(*this);
}

void Writer::write(const Report& report) {
    std::cout << report.title << '\n';
}
```

`main.cpp`

```cpp
#include "report.hpp"
#include "writer.hpp"

int main() {
    Report report{"July"};
    Writer writer;
    report.print(writer);
}
```

- Build with `c++ -std=c++17 -Wall -Wextra -pedantic main.cpp report.cpp -o report`. Running `./report` prints `July`.
- Each source file can include the two headers in either order. `<iostream>` is now an implementation detail, so a file that only includes `report.hpp` doesn't pick it up.

**Should I use `#ifndef` or `#pragma once`?**

- **`#ifndef`, `#define`, `#endif`** is standard preprocessing. Give each header a distinct, project-prefixed macro, because a reused name can silently hide an unrelated header.
- **`#pragma once`** is widely supported and has no macro name to maintain. It's an implementation extension, and file aliases can complicate how a compiler identifies a file. [Microsoft on the `once` pragma](https://learn.microsoft.com/en-us/cpp/preprocessor/once?view=msvc-170)
- The choice can follow the compilers a project supports. GCC also recognizes the conventional guard and skips rescanning the file, so speed needn't decide it. Neither form removes a dependency from the files that include the header. [GCC on once-only headers](https://gcc.gnu.org/onlinedocs/cpp/Once-Only-Headers.html)

**How do I diagnose the next header failure?**

- **A type is defined twice in one translation unit.** Check the include paths, the guard names, and whether the whole definition is inside the guard. With GCC or Clang, `c++ -std=c++17 -H -fsyntax-only main.cpp` shows the include tree.
- **A type is undeclared or incomplete.** For a pointer or reference in a declaration, a forward declaration may be enough. For a by-value member, a base class, or an inline body that uses members, include the defining header or move the body to a `.cpp`. If two classes each contain the other by value, they have no finite size, so ownership has to change.
- **Several object files define the same function at link time.** A guard starts afresh in each translation unit, so it can't help here. Declare an ordinary function in the header and define it in one `.cpp`. Inline functions and templates have different rules. [C++ one-definition rule](https://eel.is/c++draft/basic.def.odr)
- **A header only compiles after some unrelated include.** Compile a tiny source file containing only that header. If it fails, the header relies on its caller's include order, so add what it needs to the header itself. [C++ Core Guidelines on self-contained headers](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#rs-contained)

**Open**

- How much do C++20 modules change these rules in practice?
- Which tools can find unnecessary includes in a larger codebase, and how far can their suggestions be trusted?
