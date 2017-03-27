DATE_TIME_FORMAT = '%d.%m.%y @ %H:%M:%S'


def show_info_page(self, message):
    message = message
    params = {"message": message}
    return self.render_template("error", params=params)
