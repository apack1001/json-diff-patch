#!/usr/bin/env python
#-*- coding:utf-8 -*-


from __future__ import print_function

from .loader import load


#!/usr/bin/env python
# coding: utf-8

def arrayPremitiveHaveSameType(value1, value2):
    if isinstance(value1, dict) or isinstance(value2, dict):
        return False
    if isinstance(value1, list) or isinstance(value2, list):
        return False
    return True

##
# @brief When all the keys of this object are the same it take effect.
#
# @param value1 the first element
# @param value2 the second element
#
# @return True if match else False

def objectHaveCommonKeys(value1, value2):
    if (value1 == value2):
        return True
    # fix issue #27. AttributeError: 'NoneType' object has no attribute 'has_key'
    if value1 != None and value2 == None:
        return False
    if value1 == None and value2 != None:
        return False
    # issue 28. AttributeError: 'unicode' object has no attribute 'keys'
    if type(value1) == dict and type(value2) == dict:
        cntCommonKeys = 0
        for key in value1.keys():
            if value2.has_key(key):
                cntCommonKeys = cntCommonKeys + 1

        #TODO
        if (len(value1.keys()) == cntCommonKeys or len(value2.keys()) == cntCommonKeys):
            return True

        if (float(cntCommonKeys) / float(len(value1.keys())) >= 0.8):
            return True
    else:
        return False
    return False


##
# @brief Determine whether two object have common keys and object-kind child.
#
# @param value1 the first element
# @param value2 the second element
#
def haveCompositeSimilarSubkeys(value1, value2):
    if value1 == value2:
        return True

    # 1.1. value1 and value2 are not dict object
    if isinstance(value1, dict) == False or \
        isinstance(value2, dict) == False:
        return False

    # 1.2. value1 and value2 have same keys, and have dict or list child element.
    has = False
    for k in value1.keys():
        if value2.has_key(k):
            has = True
    if has:
        for k,item in value1.iteritems():
            if isinstance(item, dict) or isinstance(item, list):
                return True
        for k,item in value2.iteritems():
            if isinstance(item, dict) or isinstance(item, list):
                return True
        return False

    return value1 == value2

##
# @brief a kind of json diff algorithm named after Benjamin.
#
# This algorithm gains inspiration from an open-source project on github.
# URL: https://github.com/benjamine/jsondiffpatch/
#
# Original algorithm is described on Wikipedia.
# URL: http://en.wikipedia.org/wiki/Longest_common_subsequence_problem
#
class BenjaminJsonDiff:

    def __init__(self):
        self.result = []

    ##
    # @brief Try diff this two array child object element
    #
    # @param array1 the first array
    # @param array2 the second array
    # @param index1 the index of element in first array
    # @param index2 the index of element in second array
    # @param path the path of original array
    #
    def tryObjectInnerDiff(self, array1, array2, index1, index2, path):
        delim = '/' if path != '/' else ''
        # if isinstance(array1[index1], dict) == False or \
        #    isinstance(array2[index2], dict) == False:
        #    return
        # self.__object_diff__(array1[index1], array2[index2], delim.join([path, str(index1)]))
        self.__internal_diff__(array1[index1], array2[index2], delim.join([path, str(index1)]))
    ##
    # @brief Try diff two arrays at given path, using optimized LCS algorithm
    #
    # @param array1 child array in old json
    # @param array2 child array in new json
    # @param path the path of child array in old json
    #
    def __internal_array_diff__(self, array1, array2, path):

        def haveCompositeSimilarSubkeysByIndex(array1, array2, index1, index2):
            return haveCompositeSimilarSubkeys(array1[index1], array2[index2])

        def arrayObjectHaveCommonKeysByIndex(array1, array2, index1, index2):
            ret = objectHaveCommonKeys(array1[index1], array2[index2])
            return ret

        def arrayIndexOf(array, target):
            for index, item in enumerate(array):
                if item == target:
                    return index

            return -1

        ##
        # @brief LCS backtrack method
        #
        # @param lengthMatrix LCS matrix
        # @param array1 first array
        # @param array2 second array
        # @param index1 index in first array
        # @param index2 index in second array
        #
        # @return common sequence of this tow array and each unique slices.
        #
        def backtrack(lengthMatrix, array1, array2, index1, index2):
            if index1 == 0 and index2 == 0:
                return { 'sequence' : [ ], 'indices1' : [ ], 'indices2' : [ ] }
            # in both
            if index1 > 0 and index2 > 0 and \
                    haveCompositeSimilarSubkeysByIndex(array1, array2, index1 - 1, index2 - 1):
                subsequence = backtrack(lengthMatrix, array1, array2, index1 - 1, index2 - 1)
                subsequence['sequence'].append(array1[index1 - 1])
                subsequence['indices1'].append(index1 - 1)
                subsequence['indices2'].append(index2 - 1)
                return subsequence
            # in array1
            if index2 > 0 and (index1 == 0 or \
                    lengthMatrix[index1][index2 - 1] >= lengthMatrix[index1 - 1][index2]):
                subsequence = backtrack(lengthMatrix, array1, array2, index1, index2 - 1)
                return subsequence
            # in array2
            elif index1 > 0 and (index2 == 0 or \
                    lengthMatrix[index1][index2 - 1] < lengthMatrix[index1 - 1][index2]):
                return backtrack(lengthMatrix, array1, array2, index1 - 1, index2)


        ##
        # @brief LCS algorithm
        #
        # @param array1 first array
        # @param array2 second array
        #
        # @return LCS matrix
        def lengthMatrix(array1, array2):
            def max(lhs, rhs):
                if lhs > rhs:
                    return lhs
                return rhs

            len1 = len(array1)
            len2 = len(array2)

            # matrix[ll+1][lr+1]
            matrix = [[0 for x in range(len2 + 1)] for y in range(len1 + 1)]

            for x in range(1, len1 + 1):
                for y in range(1, len2 + 1):
                    if (haveCompositeSimilarSubkeysByIndex(array1, array2, x - 1, y - 1)):
                        matrix[x][y] = matrix[x - 1][y - 1] + 1
                    else:
                        matrix[x][y] = max(matrix[x - 1][y], matrix[x][y - 1])

            return matrix

        ##
        # @brief Interface of LCS algorithm
        #
        # @param ll the first array
        # @param rl the second array
        #
        # @return common sequence of this tow array and each unique slices.
        def __internal_lcs__(ll, rl):
            matrix = lengthMatrix(ll, rl)
            return backtrack(matrix, ll, rl, len(ll), len(rl))

        ##
        # __internal_array_diff__ started!
        commonHead = 0
        commonTail = 0
        len1 = len(array1)
        len2 = len(array2)
        delim = '/' if path != '/' else ''
        # seperate common head, perform diff to similar composite child object.
        while commonHead < len1 and commonHead < len2 and \
            haveCompositeSimilarSubkeysByIndex(array1, array2, commonHead, commonHead):
            self.tryObjectInnerDiff(array1, array2, commonHead, commonHead, path)
            commonHead = commonHead + 1

        # seperate common tail, perform diff to similar composite child object.
        while commonTail + commonHead < len1 and commonTail + commonHead < len2  and \
            haveCompositeSimilarSubkeysByIndex(array1, array2, len1 - 1 - commonTail, len2 - 1 - commonTail):
            self.tryObjectInnerDiff(array1, array2, len1 - 1 - commonTail, len2 - 1 - commonTail, path)
            commonTail = commonTail + 1

        if commonHead + commonTail == len1:
            # arrays are identical
            if len1 == len2:
                return
            # keys in array1 all exists(haveCompositeSimilarSubkeysByIndex())\
            #        in array2 and length of array2 is larger than array1
            for index in range(commonHead, len2 - commonTail):
                self.result.append({
                    #'debug' : 'common head & tail pretreatment processing -- only in array2',
                    'add': delim.join([path, str(index)]),
                    'value': array2[index],
                    'details' : 'array-item'
                    })
            return
        elif commonHead + commonTail == len2:
            for index in range(commonHead, len1 - commonTail):
                self.result.append({
                    #'debug' : 'common head & tail pretreatment processing -- only in array1',
                    'remove' : delim.join([path, str(index)]),
                    'value' : array1[index],
                    'details' : 'array-item'
                    })
            return


        # diff is not trivial, find the LCS (Longest Common Subsequence)
        lcs = __internal_lcs__(
            array1[commonHead: len1 - commonTail],
            array2[commonHead: len2 - commonTail]
            )

        # function: remove
        removedItems = []
        for index in range(commonHead, len1 - commonTail):
            indexOnLcsOfArray1 = arrayIndexOf(lcs['indices1'], index - commonHead)

            # not in first LCS-indices
            if indexOnLcsOfArray1 < 0:
                removedItems.append(index)

        # function add or move(update)
        for index in range(commonHead, len2 - commonTail):
            indexOnLcsOfArray2 = arrayIndexOf(lcs['indices2'], index - commonHead)

            # not in second LCS-indices
            if indexOnLcsOfArray2 < 0:
                # issue #2
                # patch: replace --> original: added, try to match with a removed item and register as position move
                isMove = False
                if len(removedItems) > 0:
                    for indexOfRemoved in range(0, len(removedItems)):
                        if arrayObjectHaveCommonKeysByIndex(array1, array2, removedItems[indexOfRemoved], index):
                            # issue #2 added (with a removement and an add, optimize as an object replacement)
                            # try to match with a removed item and register as position move
                            self.tryObjectInnerDiff(array1, array2, removedItems[indexOfRemoved], index, path)
                            del removedItems[indexOfRemoved]
                            isMove = True
                            break;
                            # issue #28. fix issue of [1,2,3] diff [1,4,3] return one `add` and one `remove`
                        elif arrayPremitiveHaveSameType(array1[indexOfRemoved], array2[index]):
                            self.tryObjectInnerDiff(array1, array2, removedItems[indexOfRemoved], index, path)
                            del removedItems[indexOfRemoved]
                            isMove = True
                            break;
                # real added
                if isMove == False:
                    self.result.append({
                        #'debug' : 'not move',
                        'add' : delim.join([path, str(index)]),
                        'value' : array2[index],
                        'details' : 'array-item'
                        })
            else:
                # match, in Longest Common Sequence! do inner diff
                if lcs['indices1'] != None and lcs['indices2'] != None:
                    self.tryObjectInnerDiff(array1, array2, \
                        lcs['indices1'][indexOnLcsOfArray2] + commonHead, \
                        lcs['indices2'][indexOnLcsOfArray2] + commonHead, \
                        path)

        # issue 2
        # after move-judging, it will be the final result
        for removedItem in removedItems:
            self.result.append({
                #'debug:' : 'after issue #2 judging',
                'remove' : delim.join([path, str(removedItem)]),
                'value' : array1[removedItem],
                'details' : 'array-item'
                })


    ##
    # @brief handling json array diff
    #
    # @param old child array in old json
    # @param new child array in new json
    # @param path the path of the array in old json
    #
    def __array_diff__(self, old, new, path = '/'):
        self.__internal_array_diff__(old, new, path)

    ##
    # @brief handling json object diff
    #
    # @param old child object element in old json
    # @param new child object element in new json
    # @param path the path of child object element in old json.
    #
    def __object_diff__(self, old, new, path = '/'):
        def propDiff(key):
            oval = old[key] if old.has_key(key) else None
            nval = new[key] if new.has_key(key) else None
            self.__internal_diff__(oval, nval, delim.join([path, key]))

        delim = '/' if path != '/' else ''

        for k, v in new.iteritems():
            propDiff(k)

        for k, v in old.iteritems():
            if k in new:
                continue
            propDiff(k)

    ##
    # @brief Control function of json diff algorithm. \
    #        It will recurisively call __array_diff__ and __object_diff__
    #
    # @param old the old json
    # @param new the new json
    # @param path the path of old json
    #
    def __internal_diff__(self, old, new, path = '/'):
        ##
        # handle json object element diff
        if isinstance(old, dict) and isinstance(new, dict):
            self.__object_diff__(old, new, path)
        ##
        # handle json array element diff
        elif isinstance(old, list) and isinstance(new, list):
            self.__array_diff__(old, new, path)
        ##
        # handle json premitive element diff
        else:
            if old == None and new == None:
                return
            # new value is added
            if old == None:
                self.result.append({
                    'add' : path,
                    'value': new
                    })
            # old vlaue has been removed
            else:
                if new == None:
                    self.result.append({
                        'remove': path,
                        'prev': old
                        })
                # old value has been update into new value
                else:
                    if old != new:
                        self.result.append({
                            'replace' : path,
                            'prev' : old,
                            'value' : new
                            })


    ##
    # @brief This is interface of benjamin-jsondiffpatch diff algorithm.
    #
    # @param old the old json
    # @param new the new json
    #
    # @return diff of this two object
    def diff(self, old, new):
        self.__internal_diff__(old, new)
        return self.result

def _benjamin_jsondiff(old, new):
    bjm_jsondiff = BenjaminJsonDiff()
    return bjm_jsondiff.diff(old, new)


def diff(local, other):
    return _benjamin_jsondiff(local, other)


def print_reduced(diff, pretty=True):
    """ Prints JSON diff in reduced format (similar to plain diffs).
    """

    for action in diff:
        if 'add' in action:
            print('+', action['add'], action['value'])
        elif 'remove' in action:
            print('-', action['remove'], action['prev'])


if __name__ == '__main__':
    from sys import argv, stderr
    from optparse import OptionParser
    from json_diff_patch.printer import print_json

    parser = OptionParser()
    parser.add_option('-p', '--pretty', dest='pretty', action='store_true',
                      default=False)
    parser.add_option('-j', '--json', dest='json_format', action='store_true',
                      default=False)

    (options, args) = parser.parse_args()

    if len(args) < 2:
        print('Usage:', argv[0], '[options] local_file other_file', file=stderr)
        exit(-1)

    try:
        with open(args[0]) as f:
            local = load(f)
    except IOError:
        print('Local not found', file=stderr)
        exit(-1)
    except KeyError:
        print('Path to file not specified', file=stderr)
        exit(-1)

    try:
        with open(args[1]) as f:
            other = load(f)
    except IOError:
        print('Other not found', file=stderr)
        exit(-1)
    except KeyError:
        print('Path to other file not specified', file=stderr)
        exit(-1)

    res = diff(local, other)
    if not options.json_format:
        print_reduced(res, options.pretty)
    else:
        print_json(res, "/", options.pretty)
