class PreviewFileWidget(forms.ClearableFileInput):
    template_name = "home.html"

    class Media:
        js = [
            "//code.jquery.com/jquery-3.4.1.min.js",
        ]