# Page Replacement Algorithms

## Overview
This project implements different Page Replacement Algorithms used in Operating Systems to manage memory efficiently. 
When memory frames are full and a new page needs to be loaded, the system replaces an existing page using a specific algorithm.

## Algorithms Implemented
1. FIFO (First In First Out)
2. LRU (Least Recently Used)
3. Optimal Page Replacement

## Description

### FIFO
The FIFO algorithm replaces the page that entered the memory first.

### LRU
The LRU algorithm replaces the page that has not been used for the longest period of time.

### Optimal
The Optimal algorithm replaces the page that will not be used for the longest time in the future.

## Input
- Number of frames
- Page reference string

Example:
Frames: 3  
Pages: 7 0 1 2 0 3 0 4 2 3 0 3 2

## Output
- Frame status after each page reference
- Total number of page faults

## Technologies Used
- Programming Language: C / Python
- Platform: Command Line

## Author
Swara Madichedi  
B.Tech Computer Science (IoT)  
Christ University
