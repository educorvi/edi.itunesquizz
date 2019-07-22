from plone.namedfile.utils import set_headers
from plone.namedfile.utils import stream_data
from Products.Five import BrowserView
from zope.publisher.interfaces import NotFound


class FileDownload(BrowserView):
    """ Stream file and image downloads.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """Stream BLOB of context ``file`` field to the browser.

        @param file: Blob object
        """
        blob = self.context.datei
        if blob is None:
            raise NotFound('No file present')
        # Try determine blob name and default to "context_id_download."
        # This is only visible if the user tried to save the file to local
        # computer.
        filename = getattr(blob, 'filename', self.context.id + '_download')

        # Sets Content-Type and Content-Length
        set_headers(blob, self.request.response)

        # Set Content-Disposition
        self.request.response.setHeader(
            'Content-Disposition',
            'inline; filename={0}'.format(filename)
        )
        return stream_data(blob)
