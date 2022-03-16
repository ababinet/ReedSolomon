# Reed-Solomon Encoding
Alia Babinet, Adela Dujsikova, and Lita Theng

## Overview
This project is an implementation of Reed-Solomon encoding for our CS 252: Algorithms final project at Carleton college.

## What is Reed-Solomon
Reed-Solomon is a method of error-correction, that is a way to account for a prevent potential loss of data due to physical damages to a data storage device or a noisy channel. We focused specifically on how Reed-Solomon is used in the creation of QR Codes to provide some robustness and fall-back in case of damage to the QR code. At a high level, Reed-Solomon operates by taking in a bit stream of data (what is being stored) and performs a number of mathematically complex operations on it to generate parity bits. These parity bits, are unique to the stored data, meaning that when reading the QR code, if there is a discrepency between the data and the parity bits then an error of some type must of occured. The decoding process is even more complicated as there are a number of different processes that might or might not occur depending on the nature of the data and the parity bits.

## How to use this program


