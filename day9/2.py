from dataclasses import dataclass
from typing import Optional


@dataclass
class File:
    address: int
    id: int
    size: int
    next: Optional["File"] = None
    prev: Optional["File"] = None

    def __repr__(self):
        return f"Node: address={self.address}, id={self.id}, size={self.size}, prev={self.prev.id if self.prev else None}, next={self.next.id if self.next else None}"

    def checksum(self) -> int:
        return self.id * sum(range(self.address, self.address + self.size))


with open("ex.txt") as f:
    disk_map = list(map(int, f.read()))

curr_addr = 0
tail: Optional[File] = None
files: list[File] = []  # It's still helpful to have a mapping of id:file_ptr

for i, size in enumerate(disk_map):
    if not i % 2:  # is a file
        new_file = File(
            address=curr_addr,
            id=i // 2,
            size=size,
        )
        new_file.prev = tail
        if tail:
            tail.next = new_file
        tail = new_file
        files.append(new_file)
    curr_addr += size


for mov in reversed(files):
    curr = files[0]
    while curr.address < mov.address:
        if curr.next.address - (curr.address + curr.size) >= mov.size:
            # Remove mov
            mov.prev.next = mov.next
            if mov.next:
                mov.next.prev = mov.prev
            # Update mov data
            mov.address = curr.address + curr.size
            # Insert after curr
            mov.next, mov.prev = curr.next, curr
            curr.next, mov.next.prev = mov, mov
        curr = curr.next
print(sum(f.checksum() for f in files))


def print_disk(head: File):
    s = ""
    curr = head
    while curr:
        s += str(curr.id) * curr.size
        if curr.next:
            s += "." * (curr.next.address - curr.address - curr.size)
        curr = curr.next
    print(s)
