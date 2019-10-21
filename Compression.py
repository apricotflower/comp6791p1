import Spimi
import PARAMETER
import Deal_File
from nltk.corpus import stopwords
import prettytable


def compress_number():
    no_number_tokens_sum = 0
    compress_number_document = Deal_File.all_document
    for tokens in compress_number_document.values():
        number_tokens = []
        for token in tokens:
            if token.isdigit():
                number_tokens.append(token)
        for n_tk in number_tokens:
            tokens.remove(n_tk)
        no_number_tokens_sum = no_number_tokens_sum + len(tokens)
    return no_number_tokens_sum


def case_folding():
    case_folding_document = Deal_File.all_document
    for (newid,tokens) in case_folding_document.items():
        case_folding_document[newid] = [token.lower() for token in tokens]


def stop_words(stops_words):
    no_stop_words_sum = 0
    no_stop_words_document = Deal_File.all_document
    for tokens in no_stop_words_document.values():
        stop_words_list = []
        for token in tokens:
            if token in stops_words:
                stop_words_list.append(token)
        for n_tk in stop_words_list:
            tokens.remove(n_tk)
        no_stop_words_sum = no_stop_words_sum + len(tokens)
    return no_stop_words_sum


def start_compress():
    # document = copy.deepcopy(Deal_File.all_document)
    # print("docu3:" + str(len(Deal_File.all_document)))
    print("**" * 20)
    print("unfiltered")
    # print("(distinct) terms: " + str(Spimi.terms_num))
    unfiltered_terms = Spimi.terms_num
    Spimi.terms_num = 0
    # print("nonpositional postings: " + str(Spimi.nonpositional_postings_num))
    unfiltered_nonpositional_postings = Spimi.nonpositional_postings_num
    Spimi.nonpositional_postings_num = 0
    # print("token: " + str(Deal_File.tokens_num))
    unfiltered_tokens = Deal_File.tokens_num

    print("**" * 20)
    print("Start no numbers ")
    no_number_tokens_sum = compress_number()
    Spimi.start_spimi(PARAMETER.NO_NUMBER_BLOCK_PATH, PARAMETER.NO_NUMBER_MERGE_BLOCK_PATH)
    # print("(distinct) terms: " + str(Spimi.terms_num))
    no_numbers_terms = Spimi.terms_num
    Spimi.terms_num = 0
    # print("nonpositional postings: " + str(Spimi.nonpositional_postings_num))
    no_numbers_nonpositional_postings = Spimi.nonpositional_postings_num
    Spimi.nonpositional_postings_num = 0
    # print("token: " + no_number_tokens_sum)
    no_numbers_tokens = no_number_tokens_sum

    print("**" * 20)
    print("Start case folding")
    case_folding()
    Spimi.start_spimi(PARAMETER.CASE_FOLDING_BLOCK_PATH, PARAMETER.CASE_FOLDING_MERGE_BLOCK_PATH)
    # print("(distinct) terms: " + str(Spimi.terms_num))
    case_folding_terms = Spimi.terms_num
    Spimi.terms_num = 0
    # print("nonpositional postings: " + str(Spimi.nonpositional_postings_num))
    case_folding_nonpositional_postings = Spimi.nonpositional_postings_num
    Spimi.nonpositional_postings_num = 0
    # print("token: " + no_number_tokens_sum)
    case_folding_tokens = no_number_tokens_sum

    stops = stopwords.words("english")
    print("**" * 20)
    print("30 stop words")
    stops_30 = stops[:30]
    no_stop_words_30_sum = stop_words(stops_30)
    Spimi.start_spimi(PARAMETER.STOP_WORDS_30_BLOCK_PATH, PARAMETER.STOP_WORDS_30_MERGE_BLOCK_PATH)
    # print("(distinct) terms: " + str(Spimi.terms_num))
    stop_words_30_terms = Spimi.terms_num
    Spimi.terms_num = 0
    # print("nonpositional postings: " + str(Spimi.nonpositional_postings_num))
    stop_words_30_nonpositional_postings = Spimi.nonpositional_postings_num
    Spimi.nonpositional_postings_num = 0
    # print("token: " + no_stop_words_30_sum)
    stop_words_30_tokens = no_stop_words_30_sum

    print("**" * 20)
    print("150 stop words")
    stops_150 = stops[:150]
    no_stop_words_150_sum = stop_words(stops_150)
    Spimi.start_spimi(PARAMETER.STOP_WORDS_150_BLOCK_PATH, PARAMETER.STOP_WORDS_150_MERGE_BLOCK_PATH)
    # print("(distinct) terms: " + str(Spimi.terms_num))
    stop_words_150_terms = Spimi.terms_num
    Spimi.terms_num = 0
    # print("nonpositional postings: " + str(Spimi.nonpositional_postings_num))
    stop_words_150_nonpositional_postings = Spimi.nonpositional_postings_num
    Spimi.nonpositional_postings_num = 0
    # print("token: " + no_stop_words_150_sum)
    stop_words_150_tokens = no_stop_words_150_sum

    print("Drawing Table ……")
    table = prettytable.PrettyTable()
    table.field_names = ["case", "terms_number", "term_△%", "term_T%", " nonpositional postings_number", "nonpositional postings_△%", "nonpositional postings_T%", "tokens_number", "tokens_△%", "tokens_T%"]
    table.add_row(["unfiltered", unfiltered_terms, "--", "--", unfiltered_nonpositional_postings, "--", "--", unfiltered_tokens, "--", "--"])
    table.add_row(["no numbers", no_numbers_terms, round(-100*(unfiltered_terms-no_numbers_terms)/unfiltered_terms,2),round(-100*(unfiltered_terms-no_numbers_terms)/unfiltered_terms,2), no_numbers_nonpositional_postings, round(-100*(unfiltered_nonpositional_postings-no_numbers_nonpositional_postings)/unfiltered_nonpositional_postings,2), round(-100*(unfiltered_nonpositional_postings-no_numbers_nonpositional_postings)/unfiltered_nonpositional_postings,2), no_numbers_tokens, round(-100*(unfiltered_tokens- no_numbers_tokens)/unfiltered_tokens,2), round(-100*(unfiltered_tokens- no_numbers_tokens)/unfiltered_tokens,2)])
    table.add_row(["case folding", case_folding_terms, round(-100*(no_numbers_terms-case_folding_terms)/no_numbers_terms,2), round(-100*(unfiltered_terms-case_folding_terms)/unfiltered_terms,2), case_folding_nonpositional_postings, round(-100*(no_numbers_nonpositional_postings-case_folding_nonpositional_postings)/no_numbers_nonpositional_postings,2), round(-100*(unfiltered_nonpositional_postings - case_folding_nonpositional_postings)/unfiltered_nonpositional_postings,2), case_folding_tokens, round(-100*(no_numbers_tokens-case_folding_tokens)/no_numbers_tokens,2), round(-100*(unfiltered_tokens-case_folding_tokens)/unfiltered_tokens,2)])
    table.add_row(["30 stop words", stop_words_30_terms, round(-100*(case_folding_terms-stop_words_30_terms)/case_folding_terms,2), round(-100*(unfiltered_terms-stop_words_30_terms)/unfiltered_terms,2), stop_words_30_nonpositional_postings, round(-100*(case_folding_nonpositional_postings-stop_words_30_nonpositional_postings)/case_folding_nonpositional_postings,2), round(-100*(unfiltered_nonpositional_postings-stop_words_30_nonpositional_postings)/unfiltered_nonpositional_postings,2), stop_words_30_tokens, round(-100*(case_folding_tokens-stop_words_30_tokens)/case_folding_tokens,2), round(-100*(unfiltered_tokens-stop_words_30_tokens)/unfiltered_tokens,2)])
    table.add_row(["150 stop words", stop_words_150_terms, round(-100*(case_folding_terms-stop_words_150_terms)/case_folding_terms,2), round(-100*(unfiltered_terms-stop_words_150_terms)/unfiltered_terms,2), stop_words_150_nonpositional_postings,round(-100*(case_folding_nonpositional_postings-stop_words_150_nonpositional_postings)/case_folding_nonpositional_postings,2), round(-100*(unfiltered_nonpositional_postings-stop_words_150_nonpositional_postings)/unfiltered_nonpositional_postings,2), stop_words_150_tokens, round(-100*(case_folding_tokens-stop_words_150_tokens)/case_folding_tokens,2), round(-100*(unfiltered_tokens-stop_words_150_tokens)/unfiltered_tokens,2)])

    print(table)










