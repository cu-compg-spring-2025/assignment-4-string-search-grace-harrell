def get_shift_match_table(P):
    m = len(P)
    shift_match_table = {}

    # For loop move right to left throught the string
    for shift in range(m - 1, 0, -1):
        p_1 = m - 1
        p_2 = m - shift - 1

        while p_2 >= 0:
            if P[p_2] == P[p_1]:
                p_1 -= 1
                p_2 -= 1
                if p_2 < 0:
                    shift_match_table[shift] = m - shift
                    break
            # if there is a mismatch
            else:
                shift_match_table[shift] = m - shift - p_2 - 1
                break
    shift_match_table[m] = 0
    return shift_match_table

def get_good_suffix_table(P):
    m = len(P)

    good_suffix_table = {}
    good_suffix_table[0] = 1

    shift_match_table = get_shift_match_table(P)

    for i in range(1, m + 1):
        good_suffix_table[i] = i + m

    for i in range(m, 0, -1):
        if shift_match_table[i] > 0:
            good_suffix_table[shift_match_table[i]] = i + shift_match_table[i]

    for i in range(m, 0, -1):
        if shift_match_table[i] + i == m:
            for j in range(shift_match_table[i] + 1, m+1):
                good_suffix_table[j] = min(good_suffix_table[j], j + i)
    return good_suffix_table

# Creates a lookup table that corresponds each character in the string 
# pattern with its ditance form the end of the pattern.
def get_bad_char_table(P):
    m = len(P)
    bad_char_table = {}

    unique_characters = set(P)

    for char in unique_characters:
        bad_char_table[char] = m

    for i in range(m - 1):
        bad_char_table[P[i]] = m - i - 1

    return bad_char_table



# T is the reference text and P is the pattern that we're looking for
def boyer_moore_search(T, P):
    occurrences = []
    n = len(T)
    m = len(P)
    bad_char_table = get_bad_char_table(P)
    good_suffix_table = get_good_suffix_table(P)
    
    p_1 = 0
    p_2 = 0 
    
    while p_1 <= n - m:
        p_2 = m - 1 

        while p_2 >= 0 and P[p_2] == T[p_1 + p_2]:
            p_2 -= 1

        if p_2 == -1:
            occurrences.append(p_1)
            p_1 += m
        else:
            bad_char_shift = bad_char_table.get(T[p_1 + p_2], m)
            good_suffix_shift = good_suffix_table[p_2 + 1]  # Shift based on the good suffix table
            
            # We shift by the maximum of both bad character and good suffix shifts
            p_1 += max(bad_char_shift, good_suffix_shift)
    
    return occurrences
