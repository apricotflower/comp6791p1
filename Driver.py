import Spimi
import Deal_File
import Compression
import PARAMETER
import Query
import datetime


if __name__ == '__main__':
    start = datetime.datetime.now()
    print("Start dealing with reuters ……")
    Deal_File.allfiles_break_clean()
    print("The number of articles: " + str(len(Deal_File.all_document)))
    print("Finish cleaning reuters ……")
    print("Start tokenizing ……")
    Deal_File.tokenize()
    print("Finish tokenizing ……")

    print("Start SPIMI ……")
    Spimi.start_spimi(PARAMETER.BLOCK_PATH, PARAMETER.MERGE_BLOCK_PATH)
    print("Finish SPIMI ……")

    print("Start compressing ……")
    Compression.start_compress()
    print("Finish compressing ……")

    end = datetime.datetime.now()
    print("Run time: " + str(end - start))

    print("Preparing query function……: ")
    Query.start_query()
    print("Finish")





