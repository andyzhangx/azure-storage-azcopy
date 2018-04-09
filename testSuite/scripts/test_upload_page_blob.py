import utility as util

# test_page_blob_upload_1mb verifies the azcopy upload of 1mb file
# as a page blob.
def test_page_blob_upload_1mb():
    # create the test gile.
    file_name = "test_page_blob_1mb.vhd"
    file_path = util.create_test_file(file_name, 1024*1024)

    # execute azcopy upload.
    destination = util.get_resource_sas(file_name)
    result = util.Command("copy").add_arguments(file_path).add_arguments(destination).add_flags("Logging", "5").\
                add_flags("block-size","4194304").execute_azcopy_copy_command()
    if not result:
        print("uploading file ", file_name, " failed")
        return

    # execute validator.
    result = util.Command("testBlob").add_arguments(file_path).add_arguments(destination).add_flags("blob-type", "PageBlob").execute_azcopy_verify()
    if not result:
        print("test_page_blob_upload_512B test case failed")
        return
    print("test_page_blob_upload_512B test case passed successfully")

# test_page_range_for_complete_sparse_file verifies the number of Page ranges for
# complete empty file i.e each character is Null character.
def test_page_range_for_complete_sparse_file():
    # create test file.
    file_name = "sparse_file.vhd"
    file_path = util.create_complete_sparse_file(file_name, 4 * 1024 * 1024)

    # execute azcopy page blob upload.
    destination_sas = util.get_resource_sas(file_name)
    result = util.Command("copy").add_arguments(file_path).add_arguments(destination_sas).add_flags("Logging", "5").\
        add_flags("block-size","4194304").execute_azcopy_copy_command()
    if not result:
        print("uploading file ", file_name, " failed")
        return

    # execute validator.
    # no of page ranges should be 0 for the empty sparse file.
    result = util.Command("testBlob").add_arguments(file_path).add_arguments(destination_sas).add_flags("blob-type", "PageBlob").add_flags("verify-block-size","true").add_flags("number-blocks-or-pages","0").execute_azcopy_verify()
    if not result:
        print("test_page_range_for_sparse_file test case failed")
        return
    print("test_page_range_for_sparse_file test case passed successfully")

# test_page_blob_upload_partial_sparse_file verifies the number of page ranges
# for PageBlob upload by azcopy.
def test_page_blob_upload_partial_sparse_file():
    # create test file.
    file_name = "test_partial_sparse_file.vhd"
    file_path = util.create_partial_sparse_file(file_name, 16* 1024*1024)

    # execute azcopy pageblob upload.
    destination_sas = util.get_resource_sas(file_name)
    result = util.Command("copy").add_arguments(file_path).add_arguments(destination_sas).add_flags("Logging", "5").\
                    add_flags("block-size","4194304").execute_azcopy_copy_command()
    if not result:
        print("uploading file ", file_name, " failed")
        return

    # number of page range for partial sparse created above will be (size/2)
    number_of_page_ranges = int((16* 1024*1024 / (4 * 1024 * 1024)) / 2)
    # execute validator to verify the number of page range for uploaded blob.
    result = util.Command("testBlob").add_arguments(file_path).add_arguments(destination_sas).\
        add_flags("blob-type", "PageBlob").add_flags("verify-block-size","true").\
        add_flags("number-blocks-or-pages",str(number_of_page_ranges)).execute_azcopy_verify()
    if not result:
        print("test_page_blob_upload_partial_sparse_file test case failed")
        return
    print("test_page_blob_upload_partial_sparse_file test case passed successfully")