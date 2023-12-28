
import unittest
import cfp

test "2000.rmb > 3000.dollar":
  check 2000.rmb > 3000.dollar


test "ChineseWorker[BoxLunch] > AmericanMiddleClass[Food]":
  check ChineseWorker[BoxLunch]() > AmericanMiddleClass[Food]()


test "1.爽 == 2_080_000.RMB":
  check 1.爽 == 2_080_000.rmb
