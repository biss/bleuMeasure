__author__ = 'biswajeet'

import sys
import math

class BleuMeasure:
    MAX_NGRAM = 4

    clippedHits = [0, 0, 0, 0]
    candLength = [0, 0, 0, 0]
    refLength = 0

    def addSentence(self, refTokens, candTokens):
        for i in [1,2,3,4]:
            self.saveClippedHits(i, refTokens, candTokens)
            self.candLength[i - 1] += len(candTokens) - i + 1
        self.refLength += len(refToken)

    def saveClippedHits(self, nGram, refToken, candToken):
        #dictionaries for the nGram counts
        candStats = self.constructNGrams(nGram, candToken)
        refStats = self.constructNGrams(nGram, refToken)
        print "candStats: ", candStats, sum(candStats.values())
        print "refStats: ", refStats, sum(refStats.values())

        candKeys = list(candStats.keys())
        #print "candKeys: ", candKeys

        for key in candKeys:
            refCnt = 0
            candCnt = candStats.get(key)
            if key in refStats:
                refCnt = refStats.get(key)
            self.clippedHits[nGram-1] += min(candCnt, refCnt)
            #print "for key ", key, "candCount is", candCnt, "refcnt is ", refCnt, "clipHit",(nGram-1),"is ", self.clippedHits[nGram -1 ]

    def constructNGrams(self, nGram, Tokens):
        stats = {}
        for i in range(len(Tokens)-nGram+1):
            if " ".join(Tokens[i:i+nGram]) not in stats:
                stats[" ".join(Tokens[i:i+nGram])] = 1
            else:
                stats[" ".join(Tokens[i:i+nGram])] += 1
        return stats

    def bleu(self):
        print "refLength is : ", self.refLength
        print "candLength is : ", self.candLength
        print "clippedHits is : ", self.clippedHits
        bp = 1.0 # brevity penalty
        precAvg = 0.0 # modified n-gram precisions

        if (self.candLength[0] <= self.refLength):
            bp = math.exp(1.0 - self.refLength/float(self.candLength[0]))
        print "bp: ", bp

        for i in [0,1,2,3]:
            #print "printing :", i, (self.clippedHits[i]), (self.candLength[i])
            '''if self.clippedHits[i] != 0:
                print 'candLength : ', self.candLength[i], self.clippedHits[i]
                precAvg += (1.0/4) * math.log((float(self.clippedHits[i]) + 1) / (2 * float(self.candLength[i])))
            else:
                print 'there is no matched', i, '-gram'
                return 0'''
            precAvg += (1.0/4) * math.log((float(self.clippedHits[i]) + 1) / (2 * float(self.candLength[i])))
            print "avgprec: ", precAvg

        bleu = bp * math.exp(precAvg)

        return bleu


if __name__ == '__main__':

    if len(sys.argv) != 3:
        print 'error'

    bm = BleuMeasure()

    Ref = sys.argv[1]
    Cand = sys.argv[2]
    lineCnt = 0

    with open(Ref , 'r') as r, open(Cand, 'r') as c:

        for liner, linec in zip(r, c):
            refLine = liner
            candLine = linec
            #print refLine, candLine

            refLine = refLine.strip().lower()
            candLine = candLine.strip().lower()

            refToken = refLine.split(" ")
            candToken = candLine.split(" ")

            bm.addSentence(refToken, candToken)
            lineCnt += 1

    print "Total ",lineCnt," sentence."
    print "Bleu score:",bm.bleu()
