var MONTHS = {
    0: 'Январь', 1: 'Февраль', 2: 'Март',
    3: 'Апрель', 4: 'Май', 5: 'Июнь',
    6: 'Июль', 7: 'Август', 8: 'Сентябрь',
    9: 'Октябрь', 10: 'Ноябрь', 11: 'Декабрь'
};

var DAYS = {
    1: 'Пн', 2: 'Вт', 3: 'Ср', 4: 'Чт', 5: 'Пт', 6: 'Сб', 0: 'Вс'
};

function Calendar()
{
    this.initialize = function(day){
        this.today = day || new Date();
        this.day_count = new Date(this.today.getFullYear(),
                                    this.today.getMonth()+1, 0).getDate();
        this.month = MONTHS[this.today.getMonth()];
        this.count_blank_days = new Date(this.today.getFullYear(),
                                    this.today.getMonth(), 1).getDay()-1;
        this.base_elem = $('div#calendar_base');
        if (day){
            this.__validate()
        };
    };

    this.__validate = function(){
        this.count_blank_days = this.count_blank_days <= 0 ? 6 : this.count_blank_days;
        var today = new Date();
        if (today.getFullYear() == this.today.getFullYear() &&
            today.getMonth() == this.today.getMonth())
        {
            this.today.setDate(today.getDate());
        }
    }

    this.next = function(){
        $('div.calendar_days_line').remove();
        var today = this.today.getMonth() == 11 ?
            new Date(this.today.getFullYear(), 12, 1) :
            new Date(this.today.getFullYear(), this.today.getMonth()+1, 1);
        this.initialize(day=today);
        this.build_month();
        this.set_active_day()
    }

    this.prev = function(){
        $('div.calendar_days_line').remove();
        var today = this.today.getMonth() == 0 ?
            new Date(this.today.getFullYear()-1, 11, 1) :
            new Date(this.today.getFullYear(), this.today.getMonth()-1, 1);
        this.initialize(today);
        this.build_month();
        this.set_active_day();
    };

    // toggle calendar
    this.slide = function()
    {
        $('#calendar_close').toggle();
        $(this.base_elem).slideToggle(800);
    }

    this.build_month = function()
    {
        $('#calendar_month_name').text(this.month + " " + this.today.getFullYear());
        $('#calendar_days').append($('<div>').addClass('calendar_days_line'));
        for (var day=1-this.count_blank_days, sunday=1; day<=this.day_count; ++day, ++sunday)
        {
            if (sunday == 7 || sunday == 6) {
                var new_day = $('<a>')
                .addClass('calendar_day')
                .addClass('weekend');
                sunday = sunday == 7 ? 0 : sunday;
            }
            else {
                var new_day = $('<a>')
                .addClass('calendar_day');
            };
            $(new_day).attr('href', this.create_url(day));

            if (day == this.today.getDate()
            && this.today.getMonth() == new Date().getMonth() &&
                this.today.getFullYear() == new Date().getFullYear()){ $(new_day).addClass('today')};
            $(new_day).text(day>0 ? day : '');
            $('div.calendar_days_line:last-child').append(new_day);
        };
    };

    this.create = function(prefix)
    {
        var self = this;

        this.prefix = prefix;
        this.initialize();
        this.build_month();
        this.set_navigation_listener();
        this.set_active_day();
    };

    this.format_date = function(num){
        if (num < 10){
            num = '0' + num
        };
        if (!num){
            return '01';
        }
        return num
    };

    this.set_navigation_listener = function()
    {
        var self = this;

        $('#calendar_next').click(
            function(){
                self.next();
                return false
        });
        $('#calendar_prev').click(
            function(){
                self.prev();
                return false
        });
        $('#calendar_close').click(
            function(){
                self.slide();
                return false
        });

        $('#calendar_today').attr('href', [
            self.get_category(), self.today.getFullYear(),
            self.format_date(self.today.getMonth() || 1),
            self.format_date(self.today.getDate())].join('/')
        );

        $('#calendar_week').attr('href', [
            self.get_category(), 'week'].join('/')
        );
    };

    // if a page is an event filter, the reference to the
    // events of the selected category.
    // Otherwise, the total page. 
    this.create_url = function(day){
        var url = '';
        var category = this.get_category();
        url = [this.today.getFullYear(),
               this.format_date(this.today.getMonth() + 1),
               this.format_date(day)].join('/')

        if (category){
            url = category + '/' + url;
        };
        return url;
    };

    // get active category of the event filter
    this.get_category = function(){
        var url = $('.event_types__type_active input').attr('value');
        if (!url){
            url = this.prefix;
        };
        if (url && url[url.length - 1] == '/'){
            url = url.slice(0, url.length - 1);
        }
        return url;
    };

    this.set_active_day = function set_active_day(){
        var input = $('#event__active__day');
        if (input && input.attr('value')){
            var match = /(\d{4}\/\d{1,2}\/\d{1,2})/.exec(input.attr('value'))[1];
            $("a.calendar_day[href$='" + match + "']").toggleClass('active__day');
        };
    };
};
