# -*- coding: utf-8 -*-
import sys
import codecs
import argparse
import chardet
import os
from fnmatch import fnmatchcase, fnmatch

class EncodingConversation(object):
    def __init__(self):
        self.convert_status = True

    def parser_arguments(self):
        option = argparse.ArgumentParser(description='Convert file encoding to target encoding')
        option.add_argument('-p', '--pattern', metavar='pattern', required=True, \
                            dest='pattern', action='store', help='file name pattern to convert encoding')
        option.add_argument('-o, --original', metavar='original encoding', required=False, \
                            dest='original_encoding', action='store', help='original encoding')
        option.add_argument('-t, --target', metavar='target encoding', required=True, \
                            dest='target_encoding', action='store', help='target encoding')
        option.add_argument('-c', '--case_sensitivity', dest='case_sensitivity', action='store_true', \
                            default=False, help='case sensitivity')
        option.add_argument('-d', '--detail', dest='detail_model', action='store_true', \
                            default=False, help='detail view model')

        self.args = option.parse_args()


    def fetch_file_encoding(self, file_name):
        with open(file_name, 'r') as fd:
            encoding = chardet.detect(fd.read())
        return encoding['encoding']

    def convert_file_encoding(self):
        for file_name in self.file_names:
            if self.args.original_encoding is None:
                self.args.original_encoding = self.fetch_file_encoding(file_name)
            with open(file_name, 'r') as fd:
                import tempfile
                with tempfile.NamedTemporaryFile('w+t', dir='.', delete=False) as tmp_fd:
                    for line in fd:
                        try:
                            tmp_fd.write(line.decode(self.args.original_encoding).encode(self.args.target_encoding))
                        except UnicodeDecodeError:
                            self.convert_status = False
                            self.convert_exception_message = '%s encoding cannot be used to decode' % (self.args.original_encoding)
                            break
                        except UnicodeEncodeError:
                            self.convert_status = False
                            self.convert_exception_message = '%s encoding cannot be used to encode' % (self.args.target_encoding)
                            break
                        except LookupError as e:
                            print e.message
                            os._exit(0)
                    tmp_fd_name = tmp_fd.name
            if self.convert_status is False:
                os.remove(tmp_fd_name)
                self.convert_status = True
                print '%s convert status:\t%s' % (file_name, 'failed')
                print 'exception message:\t%s' % (self.convert_exception_message)
                continue
            os.remove(file_name)
            os.rename(tmp_fd_name, file_name)
            if self.args.detail_model:
                print '%s convert status:\t%s' % (file_name, 'success')
            # else:
                # print self.fetch_file_encoding(tmp_fd_name), self.args.target_encoding
                # os.remove(tmp_fd_name)
                # print '%s convert status:\t%s' % (file_name, 'failed')




    def run(self):
        # self.fetch_file_encoding()
        self.parser_arguments()
        if self.args.case_sensitivity:
            self.file_names = [file_name for file_name in os.listdir('.') if fnmatch(file_name, self.args.pattern)]
        else:
            self.file_names = [file_name for file_name in os.listdir('.') if fnmatchcase(file_name, self.args.pattern)]
        if len(self.file_names) == 0:
            print 'No file match the pattern--"%s"' % (self.args.pattern)
            os._exit(0)

        self.convert_file_encoding()


        #
        # for file_name in file_names:
        # if args.original_encoding:
        #     try:
        #         pass
        #     except UnicodeDecodeError:
        #         pass
        # original_encoding = fetch_file_encoding('adlist.bak')
        # print 'adlist.bak encoding',original_encoding




#
# tmp = open('adlist.h', 'r')
# with open('adlist.bak', 'w+') as bak:
#     tt = tmp.read().decode('utf-8')
#     print type(tt)
#     bak.write(tt.encode('gb2312'))
# tmp.close()


con = EncodingConversation()
con.run()

# with open('adlist.bak', 'r') as bak:
#     print chardet.detect(bak.read())


# with open(self.aof_file_path, 'a+') as fd:
# fd.write(aof_buffer_string)
# fd.flush()              # ��������
# if hasattr(os, 'fdatesync'):
#     os.fdatasync(fd)        # ǿ�ƽ�fdд����̣����ǲ���ǿ�Ƹ�������Ȩ����С��Ԫ����
# else:
#     os.fsync(fd)
#
# �ļ��滻���ʺϴ��ļ�����
# with tempfile.NamedTemporaryFile('a+', dir = os.path.dirname(self.aof_file_path), delete = False) as temp_fd:
# temp_fd.write(aof_buffer_string)
# temp_fd_name = temp_fd.name
# print temp_fd_name
# if os.path.isfile(self.aof_file_path):
# os.remove(self.aof_file_path)