---
title: Instructions
description: Instructions
---

## 1. INBOX

Throws away what's currently in hand and takes one box (item) from the input belt. If there's nothing to take, ends the program.

## 2. OUTBOX

Put what's currently in hand onto the output belt. If there's nothing to put, throws an error.

## 3. JUMP &lt;tag&gt;

Jumps to another place and continue running the progran from there.

## 4. COPYTO &lt;slot&gt;

Copies what's currently in hand into the given slot. Throws an error if there's nothing to copy.

## 5. COPYFROM &lt;slot&gt;

Copies what's in the given slot onto hand. Throws an error if there's nothing to copy.

## 6. ADD &lt;slot&gt;

Adds what's in the given slot onto what's in hand. Throws an error unless both the slot and the hand hold a numeric value.

## 7. SUB &lt;slot&gt;

Subtractd what's in the given slot from what's in hand. Throws an error unless both the slot and the hand hold the same type of value (both numerics, or both alphabetics). If both are letters, the result is their alphabetical difference.

## 8. JUMPZ &lt;tag&gt;

Jump only when a zero is hold in hand. Does nothing when holding something else. Throws an error if the hand is empty.

## 9. JUMPN &lt;tag&gt;

Jump only when holding a negative number. Does nothing when holding a zero or a positive number. Throws an error when holding a letter or with an empty hand.

## 10. BUMP+ &lt;slot&gt;

Increments the number in the given slot by one and copy the result to hand. Throws an error if the slot is empty or contains a letter.

## 11. BUMP- &lt;slot&gt;

Decrements the number in the given slot by one and copy the result to hand. Throws an error if the slot is empty or contains a letter.
