from rest_framework.renderers import JSONRenderer
import json


class PrettyJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = super().render(data, accepted_media_type, renderer_context)
        return json.dumps(
            json.loads(response.decode('utf-8')), indent=2, ensure_ascii=False
        ).encode('utf-8')
