# Reed-Solomon Encoding
Alia Babinet, Adela Dujsikova, and Lita Theng

## Overview
This project is an implementation of Reed-Solomon encoding for our CS 252: Algorithms final project at Carleton college.

## What is Reed-Solomon
Reed-Solomon is a method of error-correction, that is a way to account for a prevent potential loss of data due to physical damages to a data storage device or a noisy channel. We focused specifically on how Reed-Solomon is used in the creation of QR Codes to provide some robustness and fall-back in case of damage to the QR code. At a high level, Reed-Solomon operates by taking in a bit stream of data (what is being stored) and performs a number of mathematically complex operations on it to generate parity bits. These parity bits, are unique to the stored data, meaning that when reading the QR code, if there is a discrepency between the data and the parity bits then an error of some type must of occured. The decoding process is even more complicated as there are a number of different processes that might or might not occur depending on the nature of the data and the parity bits.

In the context of what we have implemented here, this program is capable of the full encoding process for a given message, and is able to check if a message has been corrupted.

## How to use this program
The format for inputting to this program is as follows:

python3 reedSolomon.py <fileName> <errorSize>

*<fileName>
  This is the file that will be passed into the program containing the message. And example of this is seen in test.txt in this repository. It should be a text file that contains the message/bit stream such that each line contains a new bit. It can be in either hexidecimal or binary
  
*<errorSize>
  This is the number of error symobols which is desired. This corresponds with the robustness of the error correction (that is the amount of error correction that is occuring). This should be an integer value, for example 10.
  
If everything is inputted correctly, the corresponding encoded message will be printed out and then checked for corruption (returning a boolean value to represent if the message has been corrupted.

