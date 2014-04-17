from django.utils import six
from django.utils.six.moves.urllib.parse import quote as urlquote
                            copied=False, *args, **kwargs):
        elif (revision != PRE_CREATION and
              (not (moved or copied) or revision != '')):
        if self.lines[linenum].startswith(b"diff --git"):
        file_info.data = self.lines[linenum] + b"\n"
            file_info.origFile = GIT_DIFF_PREFIX.sub(b"", diff_line[-2])
            file_info.newFile = GIT_DIFF_PREFIX.sub(b"", diff_line[-1])

            if isinstance(file_info.origFile, six.binary_type):
                file_info.origFile = file_info.origFile.decode('utf-8')

            if isinstance(file_info.newFile, six.binary_type):
                file_info.newFile = file_info.newFile.decode('utf-8')
        # Check to make sure we haven't reached the end of the diff.
        if linenum >= len(self.lines):
            return linenum, None

            file_info.data += self.lines[linenum] + b"\n"
            file_info.data += self.lines[linenum] + b"\n"
            file_info.data += self.lines[linenum] + b"\n"
            file_info.data += self.lines[linenum + 1] + b"\n"
            file_info.data += self.lines[linenum] + b"\n"
            file_info.data += self.lines[linenum + 1] + b"\n"
            file_info.data += self.lines[linenum + 2] + b"\n"
        elif self._is_copied_file(linenum):
            file_info.data += self.lines[linenum] + b"\n"
            file_info.data += self.lines[linenum + 1] + b"\n"
            file_info.data += self.lines[linenum + 2] + b"\n"
            linenum += 3
            file_info.copied = True
            file_info.data += self.lines[linenum] + b"\n"
                file_info.data += self.lines[linenum] + b"\n"
                if self.lines[linenum].split()[1] == b"/dev/null":
                file_info.data += self.lines[linenum] + b'\n'
                file_info.data += self.lines[linenum + 1] + b'\n'
        if empty_change and not (file_info.moved or file_info.copied):
        return self.lines[linenum].startswith(b"new file mode")
        return self.lines[linenum].startswith(b"deleted file mode")
        return (self.lines[linenum].startswith(b"old mode")
                and self.lines[linenum + 1].startswith(b"new mode"))

    def _is_copied_file(self, linenum):
        return (self.lines[linenum].startswith(b'similarity index') and
                self.lines[linenum + 1].startswith(b'copy from') and
                self.lines[linenum + 2].startswith(b'copy to'))
        return (self.lines[linenum].startswith(b"similarity index") and
                self.lines[linenum + 1].startswith(b"rename from") and
                self.lines[linenum + 2].startswith(b"rename to"))
                self.lines[linenum].startswith(b"index "))
        return self.lines[linenum].startswith(b'diff --git')
        return (line.startswith(b"Binary file") or
                line.startswith(b"GIT binary patch"))
                (self.lines[linenum].startswith(b'--- ') and
                    self.lines[linenum + 1].startswith(b'+++ ')))
                raise SCMError("path must be supplied if revision is %s"
                               % HEAD)