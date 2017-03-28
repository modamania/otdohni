/*
 * ZForms client-side
 * ------------------------------------
 * @version: 3.0.4
 * @build: 3453, 2009-07-26 02:00:41
 * @author: Filatov Dmitry <alpha@zforms.ru>
 */

var ZForms = {EVENT_TYPE_ON_INIT:"zf:oninit", EVENT_TYPE_ON_CHANGE:"zf:onchange", EVENT_TYPE_ON_BEFORE_SUBMIT:"zf:onbeforesubmit", EVENT_TYPE_ON_READY_CHANGE:"zf:onreadychange", createWidget:function () {
    return new arguments[0](arguments[1][0], arguments[1][1], arguments[1][2])
}, createTextInput:function () {
    return this.createWidget(ZForms.Widget.Text, arguments)
}, createNumberInput:function () {
    return this.createWidget(ZForms.Widget.Text.Number, arguments)
}, createSelectInput:function () {
    return this.createWidget(ZForms.Widget.Select, arguments)
}, createComboInput:function () {
    return this.createWidget(ZForms.Widget.Text.Combo, arguments)
}, createContainer:function () {
    return this.createWidget(ZForms.Widget.Container, arguments)
}, createDateInput:function () {
    return this.createWidget(ZForms.Widget.Container.Date, arguments)
}, createInputGroup:function () {
    var b = this.createWidget(arguments[0], arguments[1]);
    if (arguments[1][3]) {
        for (var a = 0; a < arguments[1][3].length; a++) {
            b.addChild(this.createStateInput(arguments[1][3][a][0], arguments[1][3][a][1], arguments[1][2]))
        }
    }
    return b
}, createStateInput:function () {
    return this.createWidget(ZForms.Widget.Text.State, arguments)
}, createCheckBoxGroup:function () {
    return this.createInputGroup(ZForms.Widget.Container.Group.CheckBox, arguments)
}, createRadioButtonGroup:function () {
    return this.createInputGroup(ZForms.Widget.Container.Group.RadioButton, arguments)
}, createSlider:function () {
    return this.createWidget(ZForms.Widget.Container.Slider, arguments)
}, createSliderVertical:function () {
    return this.createWidget(ZForms.Widget.Container.Slider.Vertical, arguments)
}, createButton:function () {
    return this.createWidget(ZForms.Widget.Button, arguments)
}, createSubmitButton:function () {
    return this.createWidget(ZForms.Widget.Button.Submit, arguments)
}, createSheet:function () {
    return this.createWidget(ZForms.Widget.Container.Sheet, arguments)
}, createSheetContainer:function () {
    return this.createWidget(ZForms.Widget.Container.SheetContainer, arguments)
}, createMultiplicator:function () {
    return this.createWidget(ZForms.Widget.Container.Multiplicator, arguments)
}, createForm:function () {
    this.aForms.push(this.createWidget(ZForms.Widget.Container.Form, arguments));
    return this.aForms[this.aForms.length - 1]
}, createEnabledDependence:function (a, b) {
    return new this.Dependence.Enabled(a, b.rPattern, b.iLogic, b.bInverse, b.bFocusOnEnable)
}, createRequiredDependence:function (a, b) {
    var b = b || {};
    return new this.Dependence.Required(a, b.rPattern ? b.rPattern : (b.iMin > 1 ? new RegExp("\\S.{" + (b.iMin - 2) + ",}\\S") : /\S+/), b.iLogic, false, b.iMin)
}, createValidDependence:function (a, b) {
    var b = b || {};
    return new this.Dependence.Valid(a, b.rPattern, b.iLogic, b.bInverse, b.sClassName, b.bCheckForEmpty)
}, createValidEmailDependence:function (a, b) {
    return this.createValidDependence(a, Common.Object.extend({rPattern:/^[a-zA-Z0-9][a-zA-Z0-9\.\-\_\~]*\@[a-zA-Z0-9\.\-\_]+\.[a-zA-Z]{2,4}$/}, b))
}, createOptionsDependence:function (a, b) {
    var b = b || {};
    return new this.Dependence.Options(this.Dependence.TYPE_OPTIONS, a, b.aPatterns || [], b.iLogic)
}, createClassDependence:function (a, b) {
    var b = b || {};
    return new this.Dependence.Class(a, b.aPatternToClasses || [], b.iLogic)
}, createFunctionDependence:function (a, b) {
    var b = b || {};
    return new this.Dependence.Function(b.iType || ZForms.Dependence.TYPE_VALID, a, b.fFunction || function () {
        return true
    }, b.iLogic, b.bInverse)
}, createCompareDependence:function (a, b) {
    var b = b || {}, c = function (f, g) {
        var e = (arguments.callee.iType == ZForms.Dependence.TYPE_VALID && !arguments.callee.oOptions.bCheckForEmpty && arguments.callee.oWidget.getValue().isEmpty()) || arguments.callee.oWidget.getValue()[arguments.callee.sFunctionName](arguments.callee.mArgument instanceof ZForms.Widget ? arguments.callee.mArgument.getValue() : arguments.callee.mArgument);
        if (arguments.callee.iType == ZForms.Dependence.TYPE_VALID && arguments.callee.oOptions.sClassName) {
            g.setResult({bAdd:!e, sClassName:arguments.callee.oOptions.sClassName})
        } else {
            if (arguments.callee.iType == ZForms.Dependence.TYPE_ENABLED && arguments.callee.oOptions.bFocusOnEnable) {
                g.setResult({bFocusOnEnable:e})
            }
        }
        return e
    }, d = new this.Dependence.Function(b.iType, a, c, b.iLogic, b.bInverse);
    c.iType = b.iType;
    c.oWidget = a;
    c.mArgument = b.mArgument;
    c.sFunctionName = this.Dependence.COMPARE_FUNCTIONS[b.sCondition || "eq"];
    c.oOptions = b;
    if (!(b.mArgument instanceof ZForms.Widget)) {
        return d
    }
    return[d, new this.Dependence.Function(b.iType, b.mArgument, c, b.iLogic, b.bInverse)]
}, createValidCompareDependence:function (a, b) {
    return this.createCompareDependence(a, Common.Object.extend({iType:this.Dependence.TYPE_VALID}, b))
}, createEnabledCompareDependence:function (a, b) {
    return this.createCompareDependence(a, Common.Object.extend({iType:this.Dependence.TYPE_ENABLED}, b))
}, buildForm:function (a) {
    return new this.Builder(a).build()
}, throwException:function (a) {
    throw ("ZForms: " + a)
}, aForms:[], getFormById:function (a) {
    return this.aForms[a]
}, bInited:false, isInited:function () {
    return this.bInited
}, attachObserver:function (c, d, b, a) {
    Common.Observable.attach(c, d, b || this);
    if ((c == this.EVENT_TYPE_ON_INIT && b == this && this.isInited()) || a) {
        d(c, b)
    } else {
        if (c == this.EVENT_TYPE_ON_READY_CHANGE) {
            d(c, b, b.isReadyForSubmit())
        }
    }
}, detachObserver:function (b, c, a) {
    Common.Observable.detach(b, c, a)
}, notifyObservers:function (b, c, a) {
    Common.Observable.notify(b, c, a)
}};
ZForms.Value = Abstract.inheritTo({__constructor:function (a) {
    this.mValue = null;
    this.reset();
    if (a != null) {
        this.set(a)
    }
}, reset:function () {
    this.set("")
}, get:function () {
    return this.mValue
}, set:function (a) {
    this.mValue = typeof(a) == "string" ? a : a.toString()
}, match:function (a) {
    return a.test(this.get())
}, clone:function () {
    var a = new this.__self();
    a.set(this.get());
    return a
}, isEqual:function (b) {
    if (!this.checkForCompareTypes(b)) {
        return false
    }
    var a = (b instanceof this.__self) ? b : new this.__self(b);
    return this.mValue === a.mValue
}, isGreater:function (b) {
    if (!this.checkForCompareTypes(b)) {
        return false
    }
    var a = (b instanceof this.__self) ? b : new this.__self(b);
    return this.get().length > a.get().length
}, isGreaterOrEqual:function (a) {
    return this.isGreater(a) || this.isEqual(a)
}, isLess:function (a) {
    return this.checkForCompareTypes(a) && !this.isGreaterOrEqual(a)
}, isLessOrEqual:function (a) {
    return this.checkForCompareTypes(a) && !this.isGreater(a)
}, checkForCompareTypes:function (a) {
    return a instanceof this.__self || typeof(a) == "string"
}, isEmpty:function () {
    return this.mValue === ""
}, toStr:function () {
    return this.get().toString()
}});
ZForms.Value.Number = ZForms.Value.inheritTo({set:function (a) {
    this.mValue = parseFloat(a.toString().replace(/[^0-9\.\,\-]/g, "").replace(/\,/g, "."))
}, match:function (a) {
    return a.test(isNaN(this.mValue) ? "" : this.mValue.toString())
}, isEmpty:function () {
    return isNaN(this.mValue)
}, isEqual:function (b) {
    if (!this.checkForCompareTypes(b)) {
        return false
    }
    var a = (b instanceof this.__self) ? b : new this.__self((b instanceof ZForms.Value) ? b.get() : b);
    return this.get() === a.get()
}, isGreater:function (b) {
    if (!this.checkForCompareTypes(b)) {
        return false
    }
    var a = (b instanceof this.__self) ? b : new this.__self((b instanceof ZForms.Value) ? b.get() : b);
    return this.get() > a.get()
}, checkForCompareTypes:function (a) {
    return a instanceof this.__self || (a instanceof ZForms.Value && !isNaN(parseFloat(a.get()))) || typeof(a) == "number" || (typeof(a) == "string" && !isNaN(parseFloat(a.toString())))
}, toStr:function () {
    return isNaN(this.mValue) ? "" : this.mValue.toString()
}});
ZForms.Value.Multiple = ZForms.Value.inheritTo({reset:function () {
    this.set([])
}, set:function (a) {
    this.mValue = a instanceof Array ? a : [a]
}, match:function (b) {
    if (this.isEmpty()) {
        return b.test("")
    }
    for (var a = 0; a < this.mValue.length; a++) {
        if (b.test(this.mValue[a])) {
            return true
        }
    }
    return false
}, clone:function () {
    var b = new this.__self();
    for (var a = 0; a < this.mValue.length; a++) {
        b.add(this.mValue[a])
    }
    return b
}, isEqual:function (c) {
    if (!(c instanceof this.__self || c instanceof Array)) {
        return this.mValue.length == 1 && this.mValue[0] === (c instanceof ZForms.Value ? c.get() : c)
    }
    var a = c instanceof this.__self ? c : new this.__self(c);
    if (this.mValue.length != a.mValue.length) {
        return false
    }
    for (var b = 0; b < this.mValue.length; b++) {
        if (this.mValue[b] != a.mValue[b]) {
            return false
        }
    }
    return true
}, isGreater:function (a) {
    if (!(a instanceof this.__self || a instanceof Array)) {
        return false
    }
    return this.get().length > (a instanceof this.__self ? a : new this.__self(a)).get().length
}, checkForCompareTypes:function (a) {
    return a instanceof this.__self || a instanceof Array
}, isEmpty:function () {
    return this.mValue.length == 0
}, add:function (a) {
    if (this.mValue.contains(a)) {
        return
    }
    this.mValue.push(a)
}, remove:function (a) {
    this.mValue.remove(a)
}});
ZForms.Value.Date = ZForms.Value.inheritTo({reset:function () {
    this.mValue = [];
    this.mValue[this.__self.PART_YEAR] = "";
    this.mValue[this.__self.PART_MONTH] = "";
    this.mValue[this.__self.PART_DAY] = ""
}, get:function () {
    if (this.isEmpty()) {
        return""
    }
    return this.getYear() + "-" + this.getMonth() + "-" + this.getDay()
}, set:function (b) {
    var c = null;
    if (b instanceof Date) {
        c = b
    } else {
        var a = b.match(/^(-?\d{1,4})-(\d{1,2})-(-?\d{1,2})/);
        if (a) {
            c = new Date(parseInt(a[1], 10), parseInt(a[2], 10) - 1, parseInt(a[3], 10))
        }
    }
    if (c) {
        this.mValue[this.__self.PART_YEAR] = c.getFullYear();
        this.mValue[this.__self.PART_MONTH] = c.getMonth() + 1;
        this.mValue[this.__self.PART_DAY] = c.getDate()
    } else {
        this.reset()
    }
}, isEqual:function (a) {
    if (a instanceof this.__self.Time) {
        return this.get() + " 0:0:0" == a.get()
    }
    if (a instanceof this.__self) {
        return this.get() == a.get()
    }
    if (a instanceof ZForms.Value) {
        return this.get() == a.get()
    }
    if (a instanceof Date) {
        return this.get() == new this.__self(a).get()
    }
    return this.get() === a
}, isGreater:function (b) {
    var a = (b instanceof ZForms.Value.Date) ? b : new ZForms.Value.Date((b instanceof ZForms.Value) ? b.get() : b);
    if (this.isEmpty() || a.isEmpty()) {
        return false
    }
    if (this.getYear() > a.getYear()) {
        return true
    }
    if (this.getYear() == a.getYear()) {
        if (this.getMonth() > a.getMonth()) {
            return true
        }
        return this.getMonth() == a.getMonth() && this.getDay() > a.getDay()
    }
    return false
}, checkForCompareTypes:function (a) {
    if (a instanceof this.__self || a instanceof this.__self.Time) {
        return !a.isEmpty()
    }
    if (a instanceof ZForms.Value) {
        return !(new ZForms.Value.Date(a.get()).isEmpty())
    }
    if (typeof(a) == "string") {
        return !(new ZForms.Value.Date(a).isEmpty())
    }
    return a instanceof Date
}, isEmpty:function () {
    return !this.mValue || this.mValue[this.__self.PART_YEAR] == "" || this.mValue[this.__self.PART_MONTH] == "" || this.mValue[this.__self.PART_DAY] == ""
}, getYear:function () {
    return this.mValue[this.__self.PART_YEAR]
}, getMonth:function () {
    return this.mValue[this.__self.PART_MONTH]
}, getDay:function () {
    return this.mValue[this.__self.PART_DAY]
}, toStr:function () {
    if (this.isEmpty()) {
        return""
    }
    return this.getYear() + "-" + (this.getMonth() < 10 ? "0" : "") + this.getMonth() + "-" + (this.getDay() < 10 ? "0" : "") + this.getDay()
}}, {PART_YEAR:"year", PART_MONTH:"month", PART_DAY:"day"});
ZForms.Value.Date.Time = ZForms.Value.Date.inheritTo({reset:function () {
    this.__base();
    this.mValue[this.__self.PART_HOUR] = "";
    this.mValue[this.__self.PART_MINUTE] = "";
    this.mValue[this.__self.PART_SECOND] = ""
}, get:function () {
    if (this.isEmpty()) {
        return""
    }
    return this.__base() + " " + this.getHour() + ":" + this.getMinute() + ":" + this.getSecond()
}, set:function (b) {
    var c = null;
    if (b instanceof Date) {
        c = b
    } else {
        var a = b.match(/^(-?\d{1,4})-(\d{1,2})-(-?\d{1,2})( (-?\d{1,2}):(-?\d{1,2}):(-?\d{1,2}))?/);
        if (a) {
            c = new Date(parseInt(a[1], 10), parseInt(a[2], 10) - 1, parseInt(a[3], 10), a[5] ? parseInt(a[5], 10) : 0, a[6] ? parseInt(a[6], 10) : 0, a[7] ? parseInt(a[7], 10) : 0)
        }
    }
    if (c) {
        this.mValue[this.__self.PART_YEAR] = c.getFullYear();
        this.mValue[this.__self.PART_MONTH] = c.getMonth() + 1;
        this.mValue[this.__self.PART_DAY] = c.getDate();
        this.mValue[this.__self.PART_HOUR] = c.getHours();
        this.mValue[this.__self.PART_MINUTE] = c.getMinutes();
        this.mValue[this.__self.PART_SECOND] = c.getSeconds()
    } else {
        this.reset()
    }
}, isEqual:function (a) {
    if (a instanceof this.__self) {
        return this.get() == a.get()
    }
    if (a instanceof ZForms.Value.Date) {
        return this.get() == a.get() + " 0:0:0"
    }
    if (a instanceof ZForms.Value || typeof(a) == "string") {
        return this.isEqual(new this.__self(typeof(a) == "string" ? a : a.get()))
    }
    if (a instanceof Date) {
        return this.get() == new this.__self(a).get()
    }
    return false
}, isGreater:function (b) {
    if (this.__base(b)) {
        return true
    }
    var a = (b instanceof this.__self) ? b : new this.__self((b instanceof ZForms.Value.Date ? b.get() + " 0:0:0" : (b instanceof ZForms.Value ? b.get() : b)));
    if (this.getDay() == a.getDay()) {
        if (this.getHour() > a.getHour()) {
            return true
        } else {
            if (this.getHour() == a.getHour()) {
                if (this.getMinute() > a.getMinute()) {
                    return true
                } else {
                    return this.getMinute() == a.getMinute() && this.getSecond() > a.getSecond()
                }
            }
        }
    }
    return false
}, checkForCompareTypes:function (a) {
    if (a instanceof this.__self || a instanceof ZForms.Value.Date) {
        return !a.isEmpty()
    }
    if (a instanceof ZForms.Value) {
        return !(new ZForms.Value.Date(a.get()).isEmpty())
    }
    if (typeof(a) == "string") {
        return !(new ZForms.Value.Date.Time(a).isEmpty())
    }
    return a instanceof Date
}, isEmpty:function () {
    return this.__base() || this.mValue[this.__self.PART_HOUR] === "" || this.mValue[this.__self.PART_MINUTE] === "" || this.mValue[this.__self.PART_SECOND] === ""
}, getHour:function () {
    return this.mValue[this.__self.PART_HOUR]
}, getMinute:function () {
    return this.mValue[this.__self.PART_MINUTE]
}, getSecond:function () {
    return this.mValue[this.__self.PART_SECOND]
}, toStr:function () {
    if (this.isEmpty()) {
        return""
    }
    return this.__base() + " " + (this.getHour() < 10 ? "0" : "") + this.getHour() + ":" + (this.getMinute() < 10 ? "0" : "") + this.getMinute() + ":" + (this.getSecond() < 10 ? "0" : "") + this.getSecond()
}}, {PART_HOUR:"hour", PART_MINUTE:"minute", PART_SECOND:"second"});
ZForms.Widget = Abstract.inheritTo({__constructor:function (b, c, a) {
    this.oElement = b;
    this.oClassElement = c || b;
    this.oOptions = a ? Common.Object.extend(this.getDefaultOptions(), a, true) : this.getDefaultOptions();
    this.sId = Common.Dom.getAttribute(b, "id") || Common.Dom.getUniqueId(b);
    this.oDependenceProcessor = new ZForms.DependenceProcessor(this);
    this.aObservers = [];
    this.oParent = null;
    this.oForm = null;
    this.bEnabled = true;
    this.bRequired = false;
    this.bValid = true;
    this.oMultiplier = null;
    this.oValue = this.createValue();
    this.setValueFromElement(true);
    this.oInitialValue = this.oValue.clone();
    this.oLastProcessedValue = this.oValue.clone();
    this.bInitialValueChanged = false;
    this.bInited = false;
    this.addHandlers()
}, getDefaultOptions:function () {
    return{bTemplate:false, bFocusOnInit:false}
}, createValue:function (a) {
    return new ZForms.Value(a)
}, addHandlers:function () {
    if (this.isTemplate()) {
        return
    }
    var a = this;

    function b(c) {
        var c = Common.Event.normalize(c);
        c.cancelBubble = true;
        a.processEvents(true)
    }

    Common.Event.add(this.oElement, this.getEventList(), b)
}, getEventList:function () {
    return[]
}, processEvents:function (c, b, a) {
    this.setValueFromElement();
    if (!(b || this.isChanged()) || this.isTemplate()) {
        return
    } else {
        this.checkForInitialValueChanged();
        this.updateLastProcessedValue()
    }
    this.notifyObservers();
    ZForms.notifyObservers(ZForms.EVENT_TYPE_ON_CHANGE, this);
    if (!a) {
        if (this.oParent) {
            this.oParent.processEvents(c, true)
        } else {
            if (c && this.oForm) {
                this.oForm.updateSubmit()
            }
        }
    }
}, isChanged:function () {
    return !this.oValue.isEqual(this.oLastProcessedValue)
}, updateLastProcessedValue:function () {
    this.oLastProcessedValue = this.oValue.clone()
}, isInitialValueChanged:function () {
    return this.bInitialValueChanged
}, checkForInitialValueChanged:function () {
    if (!this.oForm) {
        return
    }
    if (!this.isInitialValueChanged() && !this.compareValueWithInitialValue()) {
        this.oForm.increaseChangedCounter();
        this.bInitialValueChanged = true;
        this.addClass(this.__self.CLASS_NAME_CHANGED)
    } else {
        if (this.isInitialValueChanged() && this.compareValueWithInitialValue()) {
            this.oForm.decreaseChangedCounter();
            this.bInitialValueChanged = false;
            this.removeClass(this.__self.CLASS_NAME_CHANGED)
        }
    }
}, compareValueWithInitialValue:function () {
    return this.oValue.isEqual(this.oInitialValue)
}, init:function () {
    if (this.isTemplate()) {
        return
    }
    if (this.oElement.disabled) {
        this.disable()
    }
    this.processEvents(false, true);
    if (this.oMultiplier) {
        this.oMultiplier.init()
    }
    if (this.oOptions.bFocusOnInit) {
        this.focus()
    }
    this.bInited = true;
    ZForms.notifyObservers(ZForms.EVENT_TYPE_ON_INIT, this)
}, isInited:function () {
    return this.bInited
}, getValue:function () {
    return this.oValue
}, setValue:function (a) {
    if (!this.hasValue()) {
        return
    }
    this.oValue = a;
    this.processEvents(true)
}, setValueFromElement:function () {
}, hasValue:function () {
    return true
}, getId:function () {
    return this.sId
}, setId:function (a) {
    this.sId = a
}, getName:function () {
    return this.oElement.name
}, isTemplate:function () {
    return this.oOptions.bTemplate
}, addClass:function (a, b) {
    Common.Class.add(b ? b : this.oClassElement, a)
}, removeClass:function (a, b) {
    Common.Class.remove(b ? b : this.oClassElement, a)
}, replaceClass:function (b, c, a) {
    Common.Class.replace(a ? a : this.oClassElement, b, c)
}, disable:function (a) {
    if (!this.isEnabled()) {
        return false
    }
    this.bEnabled = false;
    this.oElement.disabled = true;
    this.oClassElement.disabled = true;
    this.addClass(this.__self.CLASS_NAME_DISABLED);
    if (a) {
        this.processEvents(true, true, true)
    }
    if (this.oMultiplier) {
        this.oMultiplier.disableByOuter()
    }
    return true
}, enable:function (a) {
    if (!this.allowEnable()) {
        return false
    }
    this.bEnabled = true;
    this.oElement.disabled = false;
    this.oClassElement.disabled = false;
    this.removeClass(this.__self.CLASS_NAME_DISABLED);
    if (a) {
        this.processEvents(true, true, true);
        this.updateByObservable(true)
    }
    if (this.oMultiplier) {
        this.oMultiplier.enableByOuter()
    }
    return true
}, allowEnable:function () {
    return !this.isEnabled() && !(this.oParent && !this.oParent.isEnabled())
}, isEnabled:function () {
    return this.bEnabled
}, setRequired:function () {
    this.replaceClass(this.__self.CLASS_NAME_REQUIRED_OK, this.__self.CLASS_NAME_REQUIRED);
    this.bRequired = true
}, unsetRequired:function () {
    this.replaceClass(this.__self.CLASS_NAME_REQUIRED, this.__self.CLASS_NAME_REQUIRED_OK);
    this.bRequired = false
}, isRequired:function () {
    return this.bRequired
}, setValid:function () {
    if (this.hasValue() && this.getValue().isEmpty()) {
        this.removeClass(this.bValid ? this.__self.CLASS_NAME_INVALID_OK : this.__self.CLASS_NAME_INVALID)
    } else {
        this.replaceClass(this.__self.CLASS_NAME_INVALID, this.__self.CLASS_NAME_INVALID_OK)
    }
    this.bValid = true
}, setInvalid:function () {
    this.replaceClass(this.__self.CLASS_NAME_INVALID_OK, this.__self.CLASS_NAME_INVALID);
    this.bValid = false
}, isValid:function () {
    return this.bValid
}, isReadyForSubmit:function () {
    return !this.isEnabled() || (!this.isRequired() && (!this.oForm.oOptions.bCheckForValid || this.isValid()))
}, setParent:function (a) {
    this.oParent = a
}, setForm:function (a) {
    if (this.oForm) {
        return
    }
    this.oForm = a;
    a.addWidget(this)
}, hide:function () {
    this.addClass(this.__self.CLASS_NAME_INVISIBLE)
}, show:function () {
    this.removeClass(this.__self.CLASS_NAME_INVISIBLE)
}, focus:function () {
    var b = this.oParent;
    do {
        if (b instanceof ZForms.Widget.Container.Sheet) {
            b.oParent.select(b)
        }
        b = b.oParent
    } while (b);
    try {
        this.oElement.focus()
    } catch (a) {
    }
}, attachObserver:function (a) {
    this.aObservers.push(a)
}, detachObserver:function (a) {
    this.aObservers.remove(a)
}, detachObservers:function () {
    for (var d = 0, a, c; d < this.aObservers.length;) {
        if (this.aObservers[d] == this) {
            d++;
            continue
        }
        c = this.aObservers[d];
        a = this.aObservers[d].getDependencies();
        for (var b = 0; b < a.length; b++) {
            if (a[b].getFrom() == this) {
                this.aObservers[d].removeDependence(a[b])
            }
        }
        this.detachObserver(c);
        if (c.oParent) {
            c.updateByObservable()
        }
    }
}, notifyObservers:function () {
    for (var a = 0; a < this.aObservers.length; a++) {
        this.aObservers[a].updateByObservable()
    }
}, updateByObservable:function (a) {
    this.oDependenceProcessor.process();
    if (!a && this.oParent) {
        this.oParent.oDependenceProcessor.process()
    }
}, addDependence:function (b) {
    if (b instanceof Array) {
        for (var a = 0; a < b.length; a++) {
            this.addDependence(b[a])
        }
        return
    }
    b.getFrom().attachObserver(this);
    this.oDependenceProcessor.addDependence(b)
}, removeDependence:function (a) {
    this.oDependenceProcessor.removeDependence(a)
}, getDependencies:function () {
    return this.oDependenceProcessor.getDependencies()
}, getMultiplier:function () {
    return this.oMultiplier
}, setMultiplier:function (a) {
    this.oMultiplier = a
}, updateElements:function (a) {
    this.oElement = document.getElementById(a > 0 ? this.oElement.id.match(ZForms.Widget.Container.Multiplicator.REG_EXP_REPLACE)[1] + "_" + a : this.oElement.id);
    this.oClassElement = document.getElementById(a > 0 ? this.oClassElement.id.match(ZForms.Widget.Container.Multiplicator.REG_EXP_REPLACE)[1] + "_" + a : this.oClassElement.id);
    this.updateId(this.oElement.id);
    if (this.oElement.attachEvent) {
        this.addHandlers();
        this.addExtendedHandlers()
    }
}, updateId:function (a) {
    this.oForm.removeWidget(this);
    this.setId(a);
    this.oForm.addWidget(this)
}, addId:function (a) {
    this.setId(this.addIdToElement(this.oElement, this.__self.ID_PREFIX, a));
    this.addIdToElement(this.oClassElement, this.__self.ROW_ID_PREFIX, a);
    if (this.oMultiplier) {
        this.oMultiplier.addId(a)
    }
}, addIdToElement:function (c, a, d) {
    if (!!c.getAttribute("id")) {
        return c.getAttribute("id")
    }
    var b = a + Common.Dom.getUniqueId(c) + (d > 0 ? "_" + d : "");
    c.setAttribute("id", b);
    return b
}, addChild:function (a) {
    return a
}, getCountChildrenByPattern:function () {
    return 0
}, destruct:function () {
    this.oElement = null;
    this.oClassElement = null;
    if (this.oMultiplier) {
        this.oMultiplier.destruct()
    }
}, afterClone:function () {
    this.processEvents(true, true)
}, prepareForSubmit:function () {
}, addExtendedHandlers:function () {
}, removeChild:function (a) {
}, removeChildren:function (a) {
}, enableOptionsByValue:function (b, a) {
}, clone:function (b, d, c) {
    var a = Common.Object.extend({bTemplate:false}, this.oOptions);
    return new this.__self(b, d, a)
}}, {CLASS_NAME_REQUIRED:"zf-required", CLASS_NAME_REQUIRED_OK:"zf-required-ok", CLASS_NAME_INVALID:"zf-invalid", CLASS_NAME_INVALID_OK:"zf-invalid-ok", CLASS_NAME_DISABLED:"zf-disabled", CLASS_NAME_INVISIBLE:"zf-invisible", CLASS_NAME_SELECTED:"zf-selected", CLASS_NAME_HIDDEN:"zf-hidden", CLASS_NAME_SELECTED_INITIAL:"zf-selected-initial", CLASS_NAME_CHANGED:"zf-changed", KEY_CODE_ARROW_RIGHT:39, KEY_CODE_ARROW_LEFT:37, KEY_CODE_ARROW_UP:38, KEY_CODE_ARROW_DOWN:40, KEY_CODE_PAGE_UP:33, KEY_CODE_PAGE_DOWN:34, KEY_CODE_HOME:36, KEY_CODE_END:35, KEY_CODE_ENTER:13, KEY_CODE_TAB:9, KEY_CODE_ESCAPE:27, DOM_EVENT_TYPE_KEYUP:"keyup", DOM_EVENT_TYPE_KEYDOWN:"keydown", DOM_EVENT_TYPE_KEYPRESS:"keypress", DOM_EVENT_TYPE_CLICK:"click", DOM_EVENT_TYPE_BLUR:"blur", DOM_EVENT_TYPE_FOCUS:"focus", DOM_EVENT_TYPE_CHANGE:"change", DOM_EVENT_TYPE_MOUSEDOWN:"mousedown", DOM_EVENT_TYPE_MOUSEUP:"mouseup", DOM_EVENT_TYPE_MOUSEMOVE:"mousemove", DOM_EVENT_TYPE_SELECTSTART:"selectstart", DOM_EVENT_TYPE_UNLOAD:"unload", DOM_EVENT_TYPE_BEFOREUNLOAD:"beforeunload", DOM_EVENT_TYPE_PASTE:"paste", ID_PREFIX:"input-", ROW_ID_PREFIX:"row-"});
ZForms.Widget.Container = ZForms.Widget.inheritTo({__constructor:function (b, c, a) {
    this.aChildren = [];
    this.__base(b, c, a)
}, addChild:function (b, a) {
    if (a > -1 && a < this.aChildren.length) {
        this.aChildren.splice(a, 0, b)
    } else {
        this.aChildren.push(b)
    }
    b.setParent(this);
    if (this.oForm) {
        b.setForm(this.oForm)
    }
    return b
}, removeChild:function (a) {
    a.detachObservers();
    a.removeChildren();
    this.aChildren.remove(a);
    if (this.oForm) {
        this.oForm.removeWidget(a);
        if (a.isInitialValueChanged()) {
            this.oForm.decreaseChangedCounter()
        }
    }
    a.setParent(null);
    a = null
}, removeChildren:function () {
    while (this.aChildren.length > 0) {
        this.removeChild(this.aChildren[0])
    }
}, getChildren:function () {
    return this.aChildren
}, setForm:function (c) {
    this.__base(c);
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        this.aChildren[b].setForm(c)
    }
}, disable:function (a) {
    if (!this.__base(a)) {
        return false
    }
    for (var c = 0, b = this.aChildren.length; c < b; c++) {
        this.aChildren[c].disable(true)
    }
    return true
}, enable:function (a) {
    if (!this.allowEnable()) {
        return false
    }
    this.bEnabled = true;
    for (var c = 0, b = this.aChildren.length; c < b; c++) {
        this.aChildren[c].enable(true);
        this.aChildren[c].updateByObservable(true)
    }
    this.bEnabled = false;
    this.__base(a);
    return true
}, isValid:function () {
    if (!this.__base()) {
        return false
    }
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        if (!this.aChildren[b].isValid() && this.aChildren[b].isEnabled()) {
            return false
        }
    }
    return true
}, isRequired:function () {
    if (this.__base()) {
        return true
    }
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        if (this.aChildren[b].isRequired() && this.aChildren[b].isEnabled()) {
            return true
        }
    }
    return false
}, init:function () {
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        this.aChildren[b].init()
    }
    this.__base()
}, afterClone:function () {
    this.__base();
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        this.aChildren[b].afterClone()
    }
}, hasValue:function () {
    return false
}, isChanged:function () {
    return true
}, focus:function () {
    if (this.aChildren.length > 0) {
        this.aChildren[0].focus()
    }
}, getCountChildrenByPattern:function (c) {
    var d = 0;
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        if (!this.aChildren[b].isEnabled()) {
            continue
        }
        if (this.aChildren[b] instanceof ZForms.Widget.Container) {
            if (this.aChildren[b].getCountChildrenByPattern(c) > 0) {
                d++
            }
        } else {
            if (this.aChildren[b].getValue().match(c)) {
                d++
            }
        }
    }
    return d
}, updateElements:function (c) {
    this.__base(c);
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        this.aChildren[b].updateElements(c)
    }
}, addId:function (c) {
    this.__base(c);
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        this.aChildren[b].addId(c)
    }
}, clone:function (a, d, c) {
    var b = this.__base(a, d, c);
    this.cloneChildren(b, c);
    return b
}, cloneChildren:function (d, c) {
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        d.addChild(this.aChildren[b].clone(document.getElementById(this.aChildren[b].oElement.id.match(ZForms.Widget.Container.Multiplicator.REG_EXP_REPLACE)[1] + "_" + c), document.getElementById(this.aChildren[b].oClassElement.id.match(ZForms.Widget.Container.Multiplicator.REG_EXP_REPLACE)[1] + "_" + c), c))
    }
}, destruct:function () {
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        this.aChildren[b].destruct()
    }
    this.__base()
}, prepareForSubmit:function () {
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        this.aChildren[b].prepareForSubmit()
    }
    this.__base()
}});
ZForms.Widget.Container.Sheet = ZForms.Widget.Container.inheritTo({__constructor:function (b, c, a) {
    this.__base(b, c, a);
    this.oLegendButton = null;
    this.oPrevButton = null;
    this.oNextButton = null;
    if (this.oOptions.oElementLegend) {
        this.addLegendButton(new ZForms.Widget.Button(this.oOptions.oElementLegend, null, {bTemplate:this.oOptions.bTemplate}))
    }
    if (this.oOptions.oElementPrev) {
        this.addPrevButton(new ZForms.Widget.Button(this.oOptions.oElementPrev, null, {bTemplate:this.oOptions.bTemplate}))
    }
    if (this.oOptions.oElementNext) {
        this.addNextButton(new ZForms.Widget.Button(this.oOptions.oElementNext, null, {bTemplate:this.oOptions.bTemplate}))
    }
    this.bSelected = Common.Class.match(this.oClassElement, this.__self.CLASS_NAME_SELECTED)
}, addLegendButton:function (b) {
    this.oLegendButton = b;
    this.addChild(b);
    var a = this;
    b.setHandler(function () {
        a.oParent.select(a);
        return false
    })
}, addPrevButton:function (b) {
    this.oPrevButton = b;
    this.addChild(b);
    var a = this;
    b.setHandler(function () {
        a.oParent.prev(a);
        return false
    })
}, addNextButton:function (b) {
    this.oNextButton = b;
    this.addChild(b);
    var a = this;
    b.setHandler(function () {
        a.oParent.next(a);
        return false
    })
}, setParent:function (a) {
    this.__base(a);
    if (this.isSelected()) {
        this.oParent.select(this)
    }
}, isSelected:function () {
    return this.bSelected
}, select:function () {
    this.bSelected = true;
    this.addClass(this.__self.CLASS_NAME_SELECTED);
    if (this.oLegendButton) {
        this.oLegendButton.addClass(this.__self.CLASS_NAME_SELECTED)
    }
}, unselect:function () {
    this.bSelected = false;
    this.removeClass(this.__self.CLASS_NAME_SELECTED);
    if (this.oLegendButton) {
        this.oLegendButton.removeClass(this.__self.CLASS_NAME_SELECTED)
    }
}, destruct:function () {
    if (this.oLegendButton) {
        this.oLegendButton.destruct()
    }
    if (this.oPrevButton) {
        this.oPrevButton.destruct()
    }
    if (this.oNextButton) {
        this.oNextButton.destruct()
    }
    this.__base()
}});
ZForms.Widget.Container.SheetContainer = ZForms.Widget.Container.inheritTo({__constructor:function (b, c, a) {
    this.__base(b || document.createElement("div"), c, a);
    this.iCurrentSheetIndex = 0
}, addChild:function (a) {
    if (!(a instanceof ZForms.Widget.Container.Sheet)) {
        return
    }
    return this.__base(a)
}, findSheetIndex:function (a) {
    return this.aChildren.indexOf(a)
}, select:function (a) {
    this.selectByIndex(this.findSheetIndex(a))
}, prev:function (a) {
    this.selectByIndex(this.findSheetIndex(a) - 1)
}, next:function (a) {
    this.selectByIndex(this.findSheetIndex(a) + 1)
}, selectByIndex:function (a) {
    if (!this.aChildren[a]) {
        return
    }
    this.aChildren[this.iCurrentSheetIndex].unselect();
    this.aChildren[a].select();
    this.iCurrentSheetIndex = a
}}, {CLASS_NAME_INITED:"zf-sheetcontainer-inited"});
ZForms.Widget.Container.Group = ZForms.Widget.Container.inheritTo({hasValue:function () {
    return true
}, getName:function () {
    return this.aChildren[0] ? this.aChildren[0].oElement.name : ""
}, addChild:function (a) {
    if (!(a instanceof ZForms.Widget.Text.State)) {
        return
    }
    return this.__base(a)
}, processEvents:function (d, b, a) {
    this.__base(d, b, a);
    if (!a) {
        for (var c = 0; c < this.aChildren.length; c++) {
            this.aChildren[c].updateLastProcessedValue();
            if (this.aChildren[c].isChecked()) {
                this.aChildren[c].addClass(this.__self.CLASS_NAME_SELECTED)
            } else {
                this.aChildren[c].removeClass(this.__self.CLASS_NAME_SELECTED)
            }
        }
    }
}, enable:function (a) {
    var b = this.__base(a);
    if (b && !a) {
        this.setValueFromElement()
    }
    return b
}, disable:function (a) {
    var b = this.__base(this, a);
    if (b && !a) {
        this.setValueFromElement()
    }
    return b
}, isChanged:function () {
    return this.__base()
}});
ZForms.Widget.Container.Group.CheckBox = ZForms.Widget.Container.Group.inheritTo({createValue:function (a) {
    return new ZForms.Value.Multiple(a)
}, setValue:function (b) {
    for (var c = 0, a = b.get(); c < this.aChildren.length; c++) {
        if (a.contains(this.aChildren[c].getValue().get())) {
            this.aChildren[c].check()
        } else {
            this.aChildren[c].uncheck()
        }
    }
    this.__base(b)
}, setValueFromElement:function () {
    this.oValue.reset();
    for (var a = 0; a < this.aChildren.length; a++) {
        if (this.aChildren[a].isChecked() && this.aChildren[a].isEnabled()) {
            this.oValue.add(this.aChildren[a].getValue().get())
        }
    }
    this.__base()
}, addChild:function (a) {
    if (!this.__base(a)) {
        return
    }
    if (a.isChecked()) {
        this.oValue.add(a.getValue().get());
        this.oInitialValue.add(a.getValue().get())
    }
    return a
}, enableOptionsByValue:function (g, h, b) {
    for (var e = 0, a, l, f; e < this.aChildren.length; e++) {
        l = this.aChildren[e];
        f = false;
        for (var d = 0; d < g.length; d++) {
            a = false;
            for (var c = 0; c < g[d].length && !a; c++) {
                a = l.getValue().match(g[d][c]) ? true : false
            }
            if (a) {
                if (h || d == 0) {
                    f = true
                }
            } else {
                if (!h) {
                    f = false
                }
            }
        }
        if (f) {
            if (b) {
                l.check()
            } else {
                if (this.isEnabled()) {
                    l.enable()
                }
            }
        } else {
            if (b) {
                l.uncheck()
            } else {
                l.disable()
            }
        }
    }
    this.processEvents(true)
}});
ZForms.Widget.Container.Group.RadioButton = ZForms.Widget.Container.Group.inheritTo({setValue:function (a) {
    for (var b = 0; b < this.aChildren.length; b++) {
        if (a.isEqual(this.aChildren[b].getValue())) {
            this.aChildren[b].check()
        }
    }
    this.__base(a)
}, setValueFromElement:function () {
    this.oValue.reset();
    for (var a = 0; a < this.aChildren.length; a++) {
        if (this.aChildren[a].isChecked() && this.aChildren[a].isEnabled()) {
            this.oValue.set(this.aChildren[a].getValue().get());
            break
        }
    }
    this.__base()
}, addChild:function (a) {
    if (!this.__base(a)) {
        return
    }
    if (a.isChecked()) {
        this.oValue.set(a.getValue().get());
        this.oInitialValue.set(a.getValue().get())
    }
    return a
}, enableOptionsByValue:function (h, l) {
    var b = false, d = -1;
    for (var f = 0, a, m, g; f < this.aChildren.length; f++) {
        m = this.aChildren[f];
        g = false;
        for (var e = 0; e < h.length; e++) {
            a = false;
            for (var c = 0; c < h[e].length && !a; c++) {
                a = m.getValue().match(h[e][c]) ? true : false
            }
            if (a) {
                if (d < 0) {
                    d = f
                }
                if (l || e == 0) {
                    g = true
                }
            } else {
                if (!l) {
                    g = false
                }
            }
        }
        if (g && this.isEnabled()) {
            m.enable()
        } else {
            if (m.isEnabled()) {
                m.disable()
            }
        }
        if (!m.isEnabled() && m.isChecked()) {
            b = true
        }
    }
    if (b && d > -1) {
        this.oValue.set(this.aChildren[d].getValue());
        this.aChildren[d].check()
    }
    this.processEvents(true)
}});
ZForms.Widget.Text = ZForms.Widget.inheritTo({__constructor:function (b, c, a) {
    this.__base(b, c, a);
    this.bPlaceHolderEnabled = false;
    this.iMaxLength = this.oOptions.iMaxLength ? this.oOptions.iMaxLength : (b.maxLength > 0 ? b.maxLength : 0);
    this.bTextArea = this.oElement.tagName.toLowerCase() == "textarea";
    this.bNeedReplaceType = this.hasPlaceHolder() && this.oElement.type.toLowerCase() == "password";
    this.oPasswordReplacerElement = this.createPasswordElement();
    if (!this.isTemplate()) {
        this.addExtendedHandlers()
    }
}, getDefaultOptions:function () {
    return Common.Object.extend(this.__base(), {sPlaceHolder:""}, true)
}, updateElementValue:function (a) {
    if (a.isEmpty() && this.bPlaceHolderEnabled) {
        return
    }
    this.oElement.value = a.toStr()
}, setValue:function (a) {
    if (a.isEmpty()) {
        this.updateElementValue(a);
        this.enablePlaceHolder()
    } else {
        this.disablePlaceHolder();
        this.updateElementValue(this.processValueMaxLength(a))
    }
    this.__base(a)
}, getEventList:function () {
    return[this.__self.DOM_EVENT_TYPE_KEYUP, this.__self.DOM_EVENT_TYPE_BLUR, this.__self.DOM_EVENT_TYPE_CHANGE]
}, setValueFromElement:function () {
    if (!this.oElement) {
        return
    }
    if (this.bPlaceHolderEnabled) {
        return
    }
    this.oValue = this.processValueMaxLength(this.createValue(this.oElement.value));
    this.__base()
}, init:function () {
    if (!this.isTemplate()) {
        this.enablePlaceHolder()
    }
    this.__base()
}, focus:function () {
    if (this.oPasswordReplacerElement && this.bPlaceHolderEnabled) {
        this.oPasswordReplacerElement.focus()
    } else {
        this.__base()
    }
}, afterClone:function () {
    this.__base();
    this.enablePlaceHolder()
}, hasPlaceHolder:function () {
    return !!this.oOptions.sPlaceHolder
}, addExtendedHandlers:function () {
    if (this.isTemplate()) {
        return false
    }
    var a = this;
    this.addMaxLengthHandlers();
    Common.Event.add(this.oPasswordReplacerElement || this.oElement, this.__self.DOM_EVENT_TYPE_FOCUS, function () {
        a.addClass(a.__self.CLASS_NAME_FOCUSED);
        if (a.disablePlaceHolder() && Common.Browser.isIE()) {
            a.oElement.createTextRange().select()
        }
    });
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_BLUR, function () {
        if (a.oElement) {
            a.removeClass(a.__self.CLASS_NAME_FOCUSED);
            a.enablePlaceHolder()
        }
    });
    return true
}, addMaxLengthHandlers:function () {
    if (this.iMaxLength == 0) {
        return
    }
    if (!this.bTextArea) {
        this.oElement.maxLength = this.iMaxLength;
        return
    }
    var a = this, b;
    if (Common.Browser.isOpera() && this.oElement.isSameNode) {
        Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_KEYDOWN, function (c) {
            b = c.keyCode
        })
    }
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_KEYPRESS, function (d) {
        var d = Common.Event.normalize(d);
        if (d.iKeyCode != 13 && (d.ctrlKey || d.metaKey || d.charCode == 0 || d.which == 0 || (b == d.keyCode && (d.keyCode == 46 || d.keyCode == 45 || d.keyCode == 36 || d.keyCode == 35 || d.keyCode == 9 || d.keyCode == 8)))) {
            return
        }
        var c = document.selection ? document.selection.createRange().text.length : a.oElement.selectionEnd - a.oElement.selectionStart;
        if (c <= 0 && a.oElement.value.length >= a.iMaxLength) {
            Common.Event.cancel(d)
        }
    });
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_PASTE, function () {
        setTimeout(function () {
            a.setValue(a.createValue(a.oElement.value))
        }, 0)
    });
    if (Common.Browser.isOpera()) {
        Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_BLUR, function () {
            a.setValue(a.createValue(a.oElement.value))
        })
    }
}, processValueMaxLength:function (a) {
    if (this.iMaxLength == 0) {
        return a
    }
    if (a.toStr().length > this.iMaxLength) {
        a.set(a.get().toString().substr(0, this.iMaxLength))
    }
    return a
}, enablePlaceHolder:function () {
    if (this.bPlaceHolderEnabled || !this.hasPlaceHolder() || !this.getValue().isEmpty()) {
        return false
    }
    this.addClass(this.__self.CLASS_NAME_PLACE_HOLDER, this.oPasswordReplacerElement || this.oElement);
    if (!this.bTextArea && this.iMaxLength > 0) {
        this.oElement.maxLength = this.oOptions.sPlaceHolder.length
    }
    this.setPasswordAttribute(false);
    if (this.oPasswordReplacerElement) {
        this.oPasswordReplacerElement.value = this.oOptions.sPlaceHolder
    } else {
        this.oElement.value = this.oOptions.sPlaceHolder
    }
    this.bPlaceHolderEnabled = true;
    return true
}, disablePlaceHolder:function () {
    if (!this.bPlaceHolderEnabled || !this.hasPlaceHolder() || !this.getValue().isEmpty()) {
        return false
    }
    this.removeClass(this.__self.CLASS_NAME_PLACE_HOLDER, this.oElement);
    if (!this.bTextArea && this.iMaxLength > 0) {
        this.oElement.maxLength = this.iMaxLength
    }
    this.oElement.value = "";
    this.setPasswordAttribute(true);
    if (this.bNeedReplaceType && Common.Browser.isOpera()) {
        this.oElement.focus()
    }
    this.bPlaceHolderEnabled = false;
    return true
}, createPasswordElement:function () {
    if (!this.bNeedReplaceType || !Common.Browser.isIE()) {
        return
    }
    return Common.Dom.createElement(this.oElement.tagName, {type:"text", name:this.oElement.name, id:this.oElement.id, "class":this.oElement.className, size:this.oElement.size, maxlength:this.oElement.maxLength, value:this.oElement.value, style:this.oElement.style.cssText})
}, setPasswordAttribute:function (b) {
    if (!this.bNeedReplaceType) {
        return
    }
    if (!this.oPasswordReplacerElement) {
        this.oElement.type = b ? "password" : "text";
        return
    }
    if (b) {
        if (!this.oPasswordReplacerElement.parentNode) {
            return
        }
        this.oPasswordReplacerElement.parentNode.replaceChild(this.oElement, this.oPasswordReplacerElement);
        var a = this;
        setTimeout(function () {
            a.oElement.focus()
        }, 0)
    } else {
        if (!this.oElement.parentNode) {
            return
        }
        this.oElement.parentNode.replaceChild(this.oPasswordReplacerElement, this.oElement)
    }
}, addId:function (a) {
    this.__base(a);
    if (this.oPasswordReplacerElement) {
        this.addIdToElement(this.oPasswordReplacerElement, this.__self.ID_PREFIX, a)
    }
}, destruct:function () {
    if (this.oPasswordReplacerElement) {
        this.oPasswordReplacerElement = null
    }
    if (this.oElement) {
        this.disablePlaceHolder()
    }
    this.__base()
}, prepareForSubmit:function () {
    this.disablePlaceHolder();
    this.__base()
}}, {CLASS_NAME_FOCUSED:"zf-focused", CLASS_NAME_PLACE_HOLDER:"zf-placeholder"});
ZForms.Widget.Text.Number = ZForms.Widget.Text.inheritTo({__constructor:function (b, c, a) {
    this.__base(b, c, a);
    this.oHiddenElement = null;
    this.iTimer = null;
    if (this.isTemplate()) {
        return
    }
    this.replaceElement(b)
}, replaceElement:function (a) {
    this.oHiddenElement = a.parentNode.insertBefore(Common.Dom.createElement("input", {type:"hidden", value:a.value}), a);
    if (a.getAttribute("id")) {
        this.oHiddenElement.setAttribute("id", "value-" + a.getAttribute("id"))
    }
    if (a.getAttribute("name")) {
        this.oHiddenElement.setAttribute("name", a.getAttribute("name"));
        a.removeAttribute("name")
    }
}, getName:function () {
    return this.oHiddenElement ? this.oHiddenElement.name : this.oElement.name
}, getDefaultOptions:function () {
    return Common.Object.extend(this.__base(), {bFloat:false, bNegative:false, iErrorTimeout:230}, true)
}, createValue:function (a) {
    return new ZForms.Value.Number(a)
}, compareValueWithInitialValue:function () {
    return this.__base() || (this.oValue.isEmpty() && this.oInitialValue.isEmpty())
}, addExtendedHandlers:function () {
    if (!this.__base()) {
        return
    }
    var a = this, b = -1;
    if (Common.Browser.isOpera() && this.oElement.isSameNode) {
        Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_KEYDOWN, function (c) {
            b = c.keyCode
        })
    }
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_KEYPRESS, function (c) {
        if (a.iTimer) {
            clearTimeout(a.iTimer);
            a.removeClass(a.__self.CLASS_NAME_INVALID_KEY)
        }
        var c = Common.Event.normalize(c);
        if (c.ctrlKey || c.metaKey || c.charCode == 0 || c.which == 0 || (b == c.keyCode && (c.keyCode == 46 || c.keyCode == 45 || c.keyCode == 36 || c.keyCode == 35 || c.keyCode == 9 || c.keyCode == 8)) || c.keyCode == 13 || (c.iKeyCode >= 48 && c.iKeyCode <= 57) || (a.oOptions.bFloat && (c.iKeyCode == 44 || c.iKeyCode == 46) && !/\.|\,/.test(a.oElement.value)) || (a.oOptions.bNegative && c.iKeyCode == 45 && a.oElement.value.charAt(0) != "-" && a.getCursorPosition() == 0)) {
            return
        }
        Common.Event.cancel(c);
        a.addClass(a.__self.CLASS_NAME_INVALID_KEY);
        a.iTimer = setTimeout(function () {
            a.removeClass(a.__self.CLASS_NAME_INVALID_KEY)
        }, a.oOptions.iErrorTimeout)
    });
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_BLUR, function () {
        if (a.bPlaceHolderEnabled) {
            return
        }
        a.setValue(a.createValue(a.oElement.value))
    })
}, getCursorPosition:function () {
    if ("selectionStart" in this.oElement) {
        return this.oElement.selectionStart
    }
    if (document.selection) {
        var c = document.selection.createRange();
        if (!c) {
            return 0
        }
        var a = this.oElement.createTextRange(), b = a.duplicate();
        a.moveToBookmark(c.getBookmark());
        b.setEndPoint("EndToStart", a);
        return b.text.length
    }
    return 0
}, updateElementValue:function (a) {
    this.oHiddenElement.value = a.toStr();
    if (ZForms.Resources.getNumberSeparator() == ",") {
        a = new ZForms.Value(a.toStr().replace(/\./g, ","))
    }
    this.__base(a)
}, setValue:function (a) {
    if (!a.isEmpty()) {
        if (!this.oOptions.bFloat) {
            a.set(parseInt(a.get().toString().replace(/[\.\,].*/g, ""), 10))
        }
        if (!this.oOptions.bNegative && a.get() < 0) {
            a.set(a.get() * -1)
        }
    }
    return this.__base(a)
}, init:function () {
    this.__base();
    if (!this.bPlaceHolderEnabled) {
        this.setValue(this.getValue())
    }
}, disable:function (a) {
    if (!this.__base(a)) {
        return false
    }
    if (this.oHiddenElement) {
        this.oHiddenElement.disabled = true
    }
    return true
}, enable:function (a) {
    if (!this.__base(a)) {
        return false
    }
    if (this.oHiddenElement) {
        this.oHiddenElement.disabled = false
    }
    return true
}, destruct:function () {
    this.oHiddenElement = null;
    this.__base()
}}, {CLASS_NAME_INVALID_KEY:"zf-invalid-key"});
ZForms.Widget.Container.Date = ZForms.Widget.Container.inheritTo({__constructor:function (b, c, a) {
    this.__base(b, c, a);
    if (this.isTemplate()) {
        return
    }
    this.oDayInput = this.createNumberInput("day", 2, this.oOptions.oPlaceHolders.sDay);
    this.oMonthInput = this.createMonthInput("month");
    this.oYearInput = this.createNumberInput("year", 4, this.oOptions.oPlaceHolders.sYear);
    if (this.oOptions.bWithTime) {
        this.oHourInput = this.createNumberInput("hour", 2, this.oOptions.oPlaceHolders.sHour);
        this.oMinuteInput = this.createNumberInput("minute", 2, this.oOptions.oPlaceHolders.sMinute);
        this.oSecondInput = this.createNumberInput("second", 2, this.oOptions.oPlaceHolders.sSecond)
    }
    this.addChild(this.oDayInput);
    this.addChild(this.oMonthInput);
    this.addChild(this.oYearInput);
    if (this.oOptions.bWithTime) {
        this.addChild(this.oHourInput);
        this.addChild(this.oMinuteInput);
        this.addChild(this.oSecondInput)
    }
    this.replaceElement();
    this.setValueFromElement();
    this.addExtendedHandlers();
    this.initValue();
    this.oCalendar = this.oOptions.oPickerOpenerElement ? new ZForms.Calendar(this) : null
}, getDefaultOptions:function () {
    return Common.Object.extend(this.__base(), {bWithTime:false, bOnlyMonths:false, oPlaceHolders:{sDay:"", sYear:"", sHour:"", sMinute:"", sSecond:""}}, true)
}, createValue:function (a) {
    return this.oOptions.bWithTime ? new ZForms.Value.Date.Time(a) : new ZForms.Value.Date(a)
}, hasValue:function () {
    return true
}, setValue:function (c) {
    var d = this.oDayInput.createValue(c.getDay()), b = this.oYearInput.createValue(c.getYear());
    if ((this.oYearInput.getValue().isEmpty() || !b.isEmpty()) && !b.isEqual(this.oYearInput.getValue())) {
        this.oYearInput.setValue(b)
    }
    this.oMonthInput.setValue(this.oMonthInput.createValue(c.getMonth()));
    if ((this.oDayInput.getValue().isEmpty() || !d.isEmpty()) && !d.isEqual(this.oDayInput.getValue())) {
        this.oDayInput.setValue(d)
    }
    if (this.oOptions.bWithTime) {
        var f = this.oHourInput.createValue(c.getHour()), e = this.oMinuteInput.createValue(c.getMinute()), a = this.oSecondInput.createValue(c.getSecond());
        if ((this.oHourInput.getValue().isEmpty() || !f.isEmpty()) && !f.isEqual(this.oHourInput.getValue())) {
            this.oHourInput.setValue(f)
        }
        if ((this.oMinuteInput.getValue().isEmpty() || !e.isEmpty()) && !e.isEqual(this.oMinuteInput.getValue())) {
            this.oMinuteInput.setValue(e)
        }
        if ((this.oSecondInput.getValue().isEmpty() || !a.isEmpty()) && !a.isEqual(this.oSecondInput.getValue())) {
            this.oSecondInput.setValue(a)
        }
    }
    this.oElement.value = c.toStr();
    this.__base(c)
}, isRequired:function () {
    return ZForms.Widget.prototype.isRequired.call(this)
}, isValid:function () {
    return ZForms.Widget.prototype.isValid.call(this)
}, isChanged:function () {
    return ZForms.Widget.prototype.isChanged.call(this)
}, replaceElement:function () {
    var a = Common.Dom.createElement("input", {type:"hidden", id:this.oElement.getAttribute("id"), name:this.oElement.getAttribute("name"), value:this.oElement.value});
    this.oElement.parentNode.replaceChild(a, this.oElement);
    this.oElement = a
}, addExtendedHandlers:function () {
    if (this.isTemplate()) {
        return
    }
    var b = this, a = this.oOptions.bWithTime ? [this.oDayInput.oElement, this.oMonthInput.oElement, this.oYearInput.oElement, this.oHourInput.oElement, this.oMinuteInput.oElement, this.oSecondInput.oElement] : [this.oDayInput.oElement, this.oMonthInput.oElement, this.oYearInput.oElement];
    Common.Event.add(a, this.__self.DOM_EVENT_TYPE_BLUR, function () {
        b.processDate()
    });
    Common.Event.add(a, this.__self.DOM_EVENT_TYPE_KEYDOWN, function (c) {
        if (Common.Event.normalize(c).iKeyCode == b.__self.KEY_CODE_ENTER) {
            b.processDate()
        }
    })
}, processDate:function () {
    var d = this.oYearInput.getValue().get(), f = this.oMonthInput.getValue().get(), c = this.oDayInput.getValue().isEmpty() && this.oOptions.bOnlyMonths ? 1 : this.oDayInput.getValue().get(), b = this.oOptions.bWithTime ? this.oHourInput.getValue().get() : 0, e = this.oOptions.bWithTime ? this.oMinuteInput.getValue().get() : 0, a = this.oOptions.bWithTime ? this.oSecondInput.getValue().get() : 0;
    this.setValue(this.createValue(this.oOptions.bWithTime ? d + "-" + f + "-" + c + " " + b + ":" + e + ":" + a : d + "-" + f + "-" + c))
}, createNumberInput:function (b, c, a) {
    var d = ZForms.createNumberInput(this.oElement.parentNode.insertBefore(Common.Dom.createElement("input", {type:this.oOptions.bOnlyMonths && b == "day" ? "hidden" : "text", id:this.oElement.id ? b + "-" + this.oElement.id : "", size:c, maxlength:c, "class":"zf-input-" + b}), this.oElement), null, {sPlaceHolder:a});
    d.checkForInitialValueChanged = function () {
        return false
    };
    return d
}, createMonthInput:function (a) {
    var c = Common.Dom.createElement("select", {id:this.oElement.id ? a + "-" + this.oElement.id : "", "class":"zf-input-" + a}), e = this.oOptions.bOnlyMonths ? ZForms.Resources.getMonthsByType("normal") : ZForms.Resources.getMonthsByType("genitive");
    document.body.appendChild(c);
    c.options.length = 0;
    for (var b = 0; b < e.length; b++) {
        c.options[c.options.length] = new Option(e[b], b + 1)
    }
    var d = ZForms.createSelectInput(this.oElement.parentNode.insertBefore(document.body.removeChild(c), this.oElement));
    d.checkForInitialValueChanged = function () {
        return false
    };
    return d
}, setValueFromElement:function () {
    if (this.isTemplate() || !this.oYearInput) {
        return
    }
    this.oValue.set(this.oYearInput.getValue().get() + "-" + this.oMonthInput.getValue().get() + "-" + (this.oOptions.bOnlyMonths && this.oDayInput.getValue().isEmpty() ? 1 : this.oDayInput.getValue().get()) + (this.oOptions.bWithTime ? " " + this.oHourInput.getValue().get() + ":" + this.oMinuteInput.getValue().get() + ":" + this.oSecondInput.getValue().get() : ""));
    ZForms.Widget.prototype.setValueFromElement.call(this)
}, initValue:function () {
    this.oInitialValue = this.createValue(this.oElement.value);
    this.setValue(this.oInitialValue.clone());
    this.oDayInput.oInitialValue = this.oDayInput.createValue(this.oValue.getDay());
    this.oMonthInput.oInitialValue = this.oMonthInput.createValue(this.oValue.getMonth() || 1);
    this.oYearInput.oInitialValue = this.oYearInput.createValue(this.oValue.getYear());
    if (this.oOptions.bWithTime) {
        this.oHourInput.oInitialValue = this.oHourInput.createValue(this.oValue.getHour());
        this.oMinuteInput.oInitialValue = this.oMinuteInput.createValue(this.oValue.getMinute());
        this.oSecondInput.oInitialValue = this.oSecondInput.createValue(this.oValue.getSecond())
    }
    if (!this.getValue().isEmpty()) {
        this.addClass(this.__self.CLASS_NAME_SELECTED_INITIAL, this.oMonthInput.oElement.options[this.oMonthInput.oElement.selectedIndex])
    }
}, disable:function (a) {
    if (this.__base(a)) {
        return false
    }
    if (this.oCalendar) {
        this.oCalendar.disable()
    }
    return true
}, enable:function (a) {
    if (this.__base(a)) {
        return false
    }
    if (this.oCalendar) {
        this.oCalendar.enable()
    }
    return true
}, addId:function (a) {
    this.__base(a);
    if (this.oOptions.oPickerOpenerElement) {
        this.addIdToElement(this.oOptions.oPickerOpenerElement, "opener-", a)
    }
}, clone:function (a, c, b) {
    return new this.__self(a, c, Common.Object.extend({oPickerOpenerElement:this.oOptions.oPickerOpenerElement ? document.getElementById(this.oOptions.oPickerOpenerElement.id.match(ZForms.Widget.Container.Multiplicator.REG_EXP_REPLACE)[1] + "_" + b) : null, bTemplate:false}, this.oOptions))
}, destruct:function () {
    this.__base();
    if (this.oCalendar) {
        this.oCalendar.destruct()
    }
}});
ZForms.Widget.Text.State = ZForms.Widget.Text.inheritTo({__constructor:function (b, c, a) {
    this.__base(b, c, a);
    this.bLastProcessedChecked = null
}, getName:function () {
}, check:function () {
    this.oElement.checked = true
}, uncheck:function () {
    this.oElement.checked = false
}, isChecked:function () {
    return this.oElement.checked
}, getEventList:function () {
    return[this.__self.DOM_EVENT_TYPE_CLICK]
}, isChanged:function () {
    return this.bLastProcessedChecked != this.oElement.checked
}, updateLastProcessedValue:function () {
    this.bLastProcessedChecked = this.oElement.checked
}, addId:function (a) {
    var b = this.oParent.getChildren().indexOf(this) + 1;
    this.addIdToElement(this.oElement, this.__self.ID_PREFIX + b + "-", a);
    this.addIdToElement(this.oClassElement, this.__self.ROW_ID_PREFIX + b + "-", a)
}});
ZForms.Widget.Select = ZForms.Widget.inheritTo({__constructor:function (c, d, a) {
    this.__base(c, d, a);
    this.aOptions = [];
    for (var b = 0; b < this.oElement.options.length; b++) {
        this.aOptions[b] = {sLabel:this.oElement.options[b].innerHTML, sValue:this.oElement.options[b].value}
    }
}, setValue:function (a) {
    for (var b = 0; b < this.aOptions.length; b++) {
        if (this.aOptions[b].sValue == a.toStr()) {
            this.oElement.selectedIndex = b;
            break
        }
    }
    this.__base(a)
}, getEventList:function () {
    return[this.__self.DOM_EVENT_TYPE_CHANGE, this.__self.DOM_EVENT_TYPE_KEYUP]
}, setValueFromElement:function () {
    if (this.oElement.selectedIndex >= 0) {
        this.oValue.set(this.oElement.options[this.oElement.selectedIndex].value)
    } else {
        this.oValue.reset()
    }
    this.__base()
}, enableOptionsByValue:function (g, h) {
    this.oElement.options.length = 0;
    for (var e = 0, d, c, f; e < this.aOptions.length; e++) {
        f = this.aOptions[e];
        c = false;
        for (var b = 0; b < g.length; b++) {
            d = false;
            for (var a = 0; a < g[b].length && !d; a++) {
                d = g[b][a].test(f.sValue)
            }
            if (d) {
                if (h || b == 0) {
                    c = true
                }
            } else {
                if (!h) {
                    c = false
                }
            }
        }
        if (c) {
            this.oElement.options[this.oElement.options.length] = new Option(f.sLabel, f.sValue, this.getValue().isEqual(f.sValue))
        }
    }
    this.processEvents(true)
}});
ZForms.Widget.Text.Combo = ZForms.Widget.Text.inheritTo({__constructor:function (c, f, a) {
    if (!a.bTemplate && Common.Browser.isOpera()) {
        var e = Common.Dom.createElement("select", {name:a.oOptionsElement.name, id:a.oOptionsElement.id, "class":a.oOptionsElement.className});
        for (var b = 0, d = a.oOptionsElement.options; b < d.length; b++) {
            e.options[e.options.length] = new Option(d[b].innerHTML, d[b].value)
        }
        a.oOptionsElement.parentNode.replaceChild(e, a.oOptionsElement);
        a.oOptionsElement = e;
        a.oOptionsElement.size = this.__self.DEFAULT_PAGE_SIZE
    }
    this.oShowOptionsButton = null;
    if (!a.bTemplate && a.oShowOptionsElement) {
        a.oShowOptionsElement.tabIndex = -1;
        this.oShowOptionsButton = ZForms.createButton(a.oShowOptionsElement)
    }
    this.__base(c, f, a);
    this.oOptions.oOptionsElement = a.oOptionsElement;
    this.oOptions.oOptionsElement.tabIndex = -1;
    if (this.isTemplate()) {
        return
    }
    this.iPageSize = this.oOptions.oOptionsElement.size || this.__self.DEFAULT_PAGE_SIZE;
    Common.Class.add(this.oOptions.oOptionsElement, this.__self.CLASS_NAME_COMBO_LIST);
    this.bOptionsShowed = false;
    this.aOptions = [];
    this.aOptionsCurrent = [];
    this.oElement.setAttribute("autocomplete", "off");
    this.oOptions.oOptionsElement.setAttribute("size", this.iPageSize);
    this.iSelectedIndex = 0;
    this.sLastSearchValue = null;
    this.initOptions();
    this.hideOptions();
    this.oOptions.oOptionsElement.options.length = 0
}, addExtendedHandlers:function () {
    var b = this, c = true, a = true;
    Common.Event.add(this.oPasswordReplacerElement || this.oElement, this.__self.DOM_EVENT_TYPE_FOCUS, function () {
        b.addClass(b.__self.CLASS_NAME_FOCUSED);
        if (b.hasPlaceHolder()) {
            b.disablePlaceHolder()
        }
    });
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_KEYUP, function (d) {
        b.dispatchKeyEvent(Common.Event.normalize(d).iKeyCode)
    });
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_FOCUS, function () {
        if (!c) {
            c = true;
            return
        }
        if (b.disablePlaceHolder() && Common.Browser.isIE()) {
            b.oElement.createTextRange().select()
        }
        b.updateOptions(true)
    });
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_KEYPRESS, function (d) {
        var d = Common.Event.normalize(d);
        if (d.iKeyCode == b.__self.KEY_CODE_ENTER && b.bOptionsShowed) {
            Common.Event.cancel(d)
        }
    });
    Common.Event.add(document, this.__self.DOM_EVENT_TYPE_CLICK, function (e) {
        var d = Common.Event.normalize(e).target;
        if (d == b.oElement || (b.oOptions.oShowOptionsElement && b.oOptions.oShowOptionsElement == d)) {
            return
        }
        b.hideOptions();
        b.enablePlaceHolder()
    });
    Common.Event.add([this.oOptions.oOptionsElement, this.oElement], this.__self.DOM_EVENT_TYPE_BLUR, function () {
        if (a && b.hasPlaceHolder()) {
            b.enablePlaceHolder()
        }
        if (a && b.oElement) {
            b.removeClass(b.__self.CLASS_NAME_FOCUSED);
            b.hideOptions()
        }
        a = true
    });
    Common.Event.add(this.oOptions.oOptionsElement, this.__self.DOM_EVENT_TYPE_FOCUS, function () {
        b.showOptions()
    });
    Common.Event.add(this.oOptions.oOptionsElement, this.__self.DOM_EVENT_TYPE_CHANGE, function () {
        b.selectFromOptions();
        c = false;
        b.oElement.focus()
    });
    Common.Event.add([this.oOptions.oOptionsElement].concat(this.oOptions.oShowOptionsElement ? [this.oOptions.oShowOptionsElement] : []), this.__self.DOM_EVENT_TYPE_MOUSEDOWN, function () {
        a = false
    });
    if (this.oShowOptionsButton) {
        Common.Event.add(this.oOptions.oShowOptionsElement, this.__self.DOM_EVENT_TYPE_MOUSEUP, function () {
            a = true
        });
        this.oShowOptionsButton.setHandler(function (e) {
            b.updateOptions(true, "");
            c = false;
            b.disablePlaceHolder();
            b.oElement.focus();
            if (b.oElement.createTextRange && !Common.Browser.isOpera()) {
                var d = b.oElement.createTextRange();
                d.collapse(true);
                d.moveStart("character", 1000);
                d.moveEnd("character", 1000);
                d.select()
            }
        })
    }
}, initOptions:function () {
    var b = this.oOptions.oOptionsElement.options;
    for (var a = 0; a < b.length; a++) {
        this.aOptions[a] = {sLabel:b[a].innerHTML, sValue:b[a].value, sSearchValue:b[a].innerHTML.toLowerCase()}
    }
    this.aOptionsCurrent = this.aOptions
}, dispatchKeyEvent:function (a) {
    switch (a) {
        case this.__self.KEY_CODE_ARROW_UP:
            this.selectPrevOption();
            break;
        case this.__self.KEY_CODE_ARROW_DOWN:
            this.selectNextOption();
            break;
        case this.__self.KEY_CODE_PAGE_UP:
            this.selectPrevPage();
            break;
        case this.__self.KEY_CODE_PAGE_DOWN:
            this.selectNextPage();
            break;
        case this.__self.KEY_CODE_HOME:
            this.selectFirstOption();
            break;
        case this.__self.KEY_CODE_END:
            this.selectLastOption();
            break;
        case this.__self.KEY_CODE_ENTER:
            if (this.bOptionsShowed) {
                this.selectFromOptions()
            }
            break;
        case this.__self.KEY_CODE_TAB:
            return;
            break;
        default:
            this.updateOptions(false);
            break
    }
}, selectPrevOption:function () {
    if (this.iSelectedIndex > 0) {
        this.iSelectedIndex--
    }
    this.updateSelectedIndex()
}, selectNextOption:function () {
    if (this.iSelectedIndex < this.oOptions.oOptionsElement.options.length - 1) {
        this.iSelectedIndex++
    }
    this.updateSelectedIndex()
}, selectPrevPage:function () {
    var a = this.iSelectedIndex - this.iPageSize;
    if (a > 0) {
        this.iSelectedIndex = a
    } else {
        this.iSelectedIndex = 0
    }
    this.updateSelectedIndex()
}, selectNextPage:function () {
    var a = this.iSelectedIndex + this.iPageSize;
    if (a < this.oOptions.oOptionsElement.options.length - 1) {
        this.iSelectedIndex = a
    } else {
        this.iSelectedIndex = this.oOptions.oOptionsElement.options.length - 1
    }
    this.updateSelectedIndex()
}, selectFirstOption:function () {
    this.iSelectedIndex = 0;
    this.updateSelectedIndex()
}, selectLastOption:function () {
    this.iSelectedIndex = this.oOptions.oOptionsElement.options.length - 1;
    this.updateSelectedIndex()
}, selectFromOptions:function () {
    if (this.oOptions.oOptionsElement.options.length > 0 && this.oOptions.oOptionsElement.selectedIndex > -1) {
        if (this.hasPlaceHolder()) {
            this.disablePlaceHolder()
        }
        this.iSelectedIndex = this.oOptions.oOptionsElement.selectedIndex;
        this.sLastSearchValue = this.oElement.value.toLowerCase();
        this.setValue(new ZForms.Value(this.oOptions.oOptionsElement.options[this.iSelectedIndex].innerHTML))
    }
    var a = this;
    setTimeout(function () {
        a.hideOptions()
    }, 0)
}, updateSelectedIndex:function () {
    if (this.iSelectedIndex > -1) {
        this.oOptions.oOptionsElement.selectedIndex = this.iSelectedIndex
    }
}, updateOptions:function (f, j) {
    var g = this.oElement.value.toLowerCase(), e = typeof(j) == "undefined" ? g : j;
    if (!f && this.sLastSearchValue == e) {
        return
    }
    var c = 0, b, d = 0, k = false, h = this.oOptions.oOptionsElement, a = h.options;
    this.sLastSearchValue = e;
    a.length = 0;
    h.innerHTML = "";
    while (b = this.aOptionsCurrent[c++]) {
        if (b.sSearchValue.indexOf(e) > -1) {
            a[d++] = new Option(b.sLabel, b.sValue);
            if (g === b.sSearchValue) {
                this.iSelectedIndex = d - 1;
                k = true
            }
        }
    }
    if (!k) {
        this.iSelectedIndex = -1;
        h.selectedIndex = -1
    }
    if (d > 0) {
        this.updateSelectedIndex();
        this.showOptions()
    } else {
        this.hideOptions()
    }
}, showOptions:function () {
    if (this.bOptionsShowed) {
        return
    }
    this.addClass(this.__self.CLASS_NAME_COMBO_LIST_ACTIVE);
    this.bOptionsShowed = true
}, hideOptions:function () {
    if (!this.bOptionsShowed) {
        return
    }
    this.removeClass(this.__self.CLASS_NAME_COMBO_LIST_ACTIVE);
    this.bOptionsShowed = false
}, enableOptionsByValue:function (g, h) {
    this.aOptionsCurrent = [];
    for (var e = 0, d, c, f; e < this.aOptions.length; e++) {
        f = this.aOptions[e];
        c = false;
        for (var b = 0; b < g.length; b++) {
            d = false;
            for (var a = 0; a < g[b].length && !d; a++) {
                d = g[b][a].test(f.sValue)
            }
            if (d) {
                if (h || b == 0) {
                    c = true
                }
            } else {
                if (!h) {
                    c = false
                }
            }
        }
        if (c) {
            this.aOptionsCurrent.push(f)
        }
    }
    this.sLastSearchValue = null;
    this.iSelectedIndex = -1
}, disable:function (a) {
    if (!this.__base(a)) {
        return false
    }
    this.oOptions.oOptionsElement.disabled = true;
    if (this.oShowOptionsButton) {
        this.oShowOptionsButton.disable()
    }
    return true
}, enable:function (a) {
    if (!this.__base(a)) {
        return false
    }
    this.oOptions.oOptionsElement.disabled = false;
    if (this.oShowOptionsButton) {
        this.oShowOptionsButton.enable()
    }
    return true
}, updateElements:function (a) {
    this.oOptions.oOptionsElement = document.getElementById(a > 0 ? this.oOptions.oOptionsElement.id.match(ZForms.Widget.Container.Multiplicator.REG_EXP_REPLACE)[1] + "_" + a : this.oOptions.oOptionsElement.id);
    this.__base(a)
}, addId:function (a) {
    this.__base(a);
    this.addIdToElement(this.oOptions.oOptionsElement, "options-", a);
    if (this.oOptions.oShowOptionsElement) {
        this.addIdToElement(this.oOptions.oShowOptionsElement, "show-", a)
    }
}, clone:function (b, d, c) {
    var a = Common.Object.extend({oOptionsElement:document.getElementById(this.oOptions.oOptionsElement.id.match(ZForms.Widget.Container.Multiplicator.REG_EXP_REPLACE)[1] + "_" + c), oShowOptionsElement:this.oOptions.oShowOptionsElement ? document.getElementById(this.oOptions.oShowOptionsElement.id.match(ZForms.Widget.Container.Multiplicator.REG_EXP_REPLACE)[1] + "_" + c) : null, bTemplate:false}, this.oOptions);
    return new this.__self(b, d, a)
}, destruct:function () {
    this.oOptions.oOptionsElement = null;
    if (this.oShowOptionsButton) {
        this.oShowOptionsButton.destruct()
    }
    this.__base()
}}, {DEFAULT_PAGE_SIZE:5, CLASS_NAME_COMBO_LIST:"zf-combolist", CLASS_NAME_COMBO_LIST_ACTIVE:"zf-combolist-active"});
ZForms.Widget.Container.Slider = ZForms.Widget.Container.inheritTo({__constructor:function (c, d, b) {
    b = b || {};
    this.aSlideRules = b.aSlideRules || this.getDefaultOptions().aSlideRules;
    this.dMin = this.aSlideRules[0].dValue;
    this.dMax = this.aSlideRules[this.aSlideRules.length - 1].dValue;
    this.__base(c, d, b);
    if (this.isTemplate()) {
        return
    }
    this.aSlideRules[0].dPercent = 0;
    this.aSlideRules[this.aSlideRules.length - 1].dPercent = 100;
    var a = this.createElements(c);
    this.oContainer = a.oContainer;
    this.oScaleElement = a.oScaleElement;
    this.aControls = [];
    this.aMarks = this.createMarks(a.oScaleElement);
    this.bEnabled = true;
    this.iLastControlPosition = 0;
    this.iCurrentControlIndex = -1;
    this.iFocusedChildIndex = -1;
    this.oContainerOffset = null;
    this.fClickHandler = null;
    this.fDragStartHandler = null;
    this.fDragHandler = null;
    this.fDragEndHandler = null;
    this.fNullHandler = null;
    this.fSyncHandler = null;
    this.addExtendedHandlers();
    this.iIndex = this.__self.add(this);
    this.oLastProcessedValue = null
}, getDefaultOptions:function () {
    return Common.Object.extend(this.__base(), {aSlideRules:[
        {dValue:0, dPercent:0, dStep:1, sLabel:"0"},
        {dValue:100, dPercent:100, dStep:1, sLabel:"100"}
    ]}, true)
}, createElements:function (a) {
    var b = {oContainer:document.createElement("div"), oScaleElement:document.createElement("div"), aMarkElements:[]};
    Common.Class.add(b.oContainer, this.__self.CLASS_NAME_SLIDER);
    Common.Class.add(b.oScaleElement, this.__self.CLASS_NAME_SLIDER_SCALE);
    b.oContainer.appendChild(b.oScaleElement);
    a.insertBefore(b.oContainer, a.firstChild);
    return b
}, createMarks:function (c) {
    var d = [];
    for (var b = 0, a; b < this.aSlideRules.length; b++) {
        a = document.createElement("div");
        Common.Class.add(a, this.__self.CLASS_NAME_MARK_ELEMENT + " " + this.__self.CLASS_NAME_MARK_ELEMENT + "-" + this.aSlideRules[b].dValue);
        this.setupMarkElementPosition(a, this.aSlideRules[b].dPercent);
        if (typeof this.aSlideRules[b].sLabel != "undefined") {
            a.innerHTML = "<span>" + this.aSlideRules[b].sLabel + "</span>"
        }
        c.appendChild(a);
        d.push({oElement:a, dValue:this.aSlideRules[b].dValue, bSelected:false})
    }
    return d
}, setupMarkElementPosition:function (a, b) {
    a.style.left = b + "%"
}, createControl:function (e, b) {
    var d = {oElement:document.createElement("div"), oValueElement:document.createElement("div")}, a = this, c = this.getChildren().length - 1;
    if (e) {
        d.oElement.id = "control-" + e
    }
    Common.Class.add(d.oElement, this.__self.CLASS_NAME_CONTROL_ELEMENT + " " + this.__self.CLASS_NAME_CONTROL_ELEMENT + "-" + c);
    Common.Class.add(d.oValueElement, this.__self.CLASS_NAME_VALUE_ELEMENT);
    b.appendChild(d.oElement);
    b.appendChild(d.oValueElement);
    Common.Event.add(d.oElement, this.__self.DOM_EVENT_TYPE_MOUSEDOWN, function (f) {
        if (a.iFocusedChildIndex > -1) {
            a.aChildren[a.iFocusedChildIndex].oElement.blur()
        }
        Common.Event.cancel(f);
        a.__self.setActiveIndex(a.iIndex);
        a.fDragStartHandler(c)
    });
    return d
}, createRangeElements:function (a) {
    this.aControls[a].oLeftRangeElement = a == 0 ? this.createRangeElement(a) : this.aControls[a - 1].oRightRangeElement;
    this.aControls[a].oRightRangeElement = this.createRangeElement(a + 1)
}, createRangeElement:function (b) {
    var a = document.createElement("div");
    Common.Class.add(a, this.__self.CLASS_NAME_RANGE_ELEMENT + " " + this.__self.CLASS_NAME_RANGE_ELEMENT + "-" + b);
    this.oContainer.insertBefore(a, this.oScaleElement);
    return a
}, addChild:function (e, d) {
    if (!(e instanceof ZForms.Widget.Text.Number)) {
        return
    }
    var c = this.__base(e, d);
    if (this.isTemplate()) {
        return c
    }
    var a = this.createControl(e.oElement.id, this.oContainer);
    this.aControls.push({oElement:a.oElement, oValueElement:a.oValueElement, dPosition:null, bSelected:false});
    this.createRangeElements(this.aControls.length - 1, this.oContainer);
    var b = this, d = this.getChildren().length - 1;
    Common.Event.add(e.oElement, this.__self.DOM_EVENT_TYPE_FOCUS, function () {
        b.iFocusedChildIndex = d
    });
    Common.Event.add(e.oElement, this.__self.DOM_EVENT_TYPE_BLUR, function () {
        b.iFocusedChildIndex = -1;
        b.fSyncHandler(d)
    });
    e.setValue = function (f, g) {
        if (f.isGreater(b.getMax())) {
            f.set(b.getMax())
        } else {
            if (f.isLess(b.getMin())) {
                f.set(b.getMin())
            }
        }
        ZForms.Widget.Text.Number.prototype.setValue.call(e, f);
        if (!g) {
            b.fSyncHandler(d)
        }
    };
    e.disable = function (f) {
        if (!ZForms.Widget.prototype.disable.call(this, f)) {
            return false
        }
        b.disableControlByIndex(d)
    };
    e.enable = function (f) {
        if (!ZForms.Widget.prototype.enable.call(this, f)) {
            return false
        }
        b.enableControlByIndex(d)
    };
    this.setCurrentControlIndex(d);
    this.setValue(e.getValue());
    return c
}, addExtendedHandlers:function () {
    var a = this;
    this.fClickHandler = function (b) {
        var b = Common.Event.normalize(b), c = a.getNearestControlIndex(b);
        if (c < 0) {
            return c
        }
        a.__self.setActiveIndex(a.iIndex);
        a.setCurrentControlIndex(c);
        a.drag(b);
        return c
    };
    this.fDragStartHandler = function (b) {
        a.dragStart(b)
    };
    this.fDragHandler = function (b) {
        a.drag(Common.Event.normalize(b))
    };
    this.fDragEndHandler = function (b) {
        a.dragEnd(Common.Event.normalize(b))
    };
    this.fNullHandler = function (b) {
        Common.Event.cancel(b)
    };
    this.fSyncHandler = function (b) {
        a.setCurrentControlIndex(b);
        a.setValue(a.getChildren()[b].getValue(), true)
    };
    Common.Event.add(this.oContainer, this.__self.DOM_EVENT_TYPE_MOUSEDOWN, function (b) {
        Common.Event.cancel(b);
        if (a.iFocusedChildIndex > -1) {
            a.aChildren[a.iFocusedChildIndex].oElement.blur()
        }
        var c = a.fClickHandler(b);
        if (c >= 0) {
            a.fDragStartHandler(c)
        }
    })
}, getMin:function () {
    return this.dMin
}, getMax:function () {
    return this.dMax
}, getCurrentControl:function () {
    return this.aControls[this.iCurrentControlIndex]
}, getCurrentControlIndex:function () {
    return this.iCurrentControlIndex
}, setCurrentControlIndex:function (a) {
    if (this.getCurrentControlIndex() == a) {
        return
    }
    if (this.getCurrentControlIndex() > -1) {
        Common.Class.remove(this.getCurrentControl().oElement, this.__self.CLASS_NAME_CONTROL_ELEMENT_SELECTED)
    }
    this.iCurrentControlIndex = a;
    Common.Class.add(this.getCurrentControl().oElement, this.__self.CLASS_NAME_CONTROL_ELEMENT_SELECTED)
}, getNearestControlIndex:function (a) {
    this.updateContainerOffset();
    var b = this.calculateValueByOffset(this.calculateOffset(a)), e = -1, g = Math.abs(this.getMax() - this.getMin()), c = 0, d, f;
    while (d = this.aChildren[c++]) {
        if (!d.isEnabled()) {
            continue
        }
        f = Math.abs(d.getValue().get() - b.get());
        if (f < g || (Math.abs(f - g) < 0.00001 && d.getValue().get() < b.get())) {
            g = f;
            e = c - 1
        }
    }
    return e
}, dragStart:function (a) {
    if (!this.isEnabled() || !this.getChildren()[a].isEnabled()) {
        return false
    }
    this.setCurrentControlIndex(a);
    this.updateContainerOffset();
    Common.Event.add(document, this.__self.DOM_EVENT_TYPE_SELECTSTART, this.fNullHandler);
    Common.Event.add(document, this.__self.DOM_EVENT_TYPE_MOUSEMOVE, this.fDragHandler);
    Common.Event.add(document, this.__self.DOM_EVENT_TYPE_MOUSEUP, this.fDragEndHandler)
}, drag:function (a) {
    if (!this.isEnabled()) {
        return false
    }
    this.updateContainerOffset();
    this.setValue(this.calculateValueByOffset(this.calculateOffset(a)))
}, dragEnd:function () {
    Common.Event.remove(document, this.__self.DOM_EVENT_TYPE_MOUSEMOVE, this.fDragHandler);
    Common.Event.remove(document, this.__self.DOM_EVENT_TYPE_MOUSEUP, this.fDragEndHandler);
    Common.Event.remove(document, this.__self.DOM_EVENT_TYPE_SELECTSTART, this.fNullHandler)
}, setValue:function (g, h) {
    if (!this.getCurrentControl()) {
        return
    }
    var e = this.findSlideRuleIndexByValue(g), b = this.getSlideRuleByIndex(e), k = this.getSlideRuleByIndex(e - 1), f = this.getSlideRuleByIndex(e + 1), c = parseFloat((Math.round((g.get() - b.dValue) / b.dStep) * b.dStep + b.dValue).toFixed(8)), a = this.getChildren()[this.getCurrentControlIndex() - 1], d = this.getChildren()[this.getCurrentControlIndex() + 1], j;
    if (k && c < k.dValue) {
        c = k.dValue
    } else {
        if (f && c > f.dValue) {
            c = f.dValue
        }
    }
    if (c < this.getMin()) {
        c = this.getMin()
    }
    if (a && a.getValue().get() > c) {
        if (h && this.getChildren()[this.getCurrentControlIndex() - 1].isEnabled()) {
            j = this.getChildren()[this.getCurrentControlIndex()];
            j.setValue(j.createValue(parseFloat(c)), true);
            --this.iCurrentControlIndex;
            this.setValue(j.createValue(parseFloat(c)), h);
            ++this.iCurrentControlIndex
        }
        c = a.getValue().get()
    } else {
        if (d && d.getValue().get() < c) {
            if (h && this.getChildren()[this.getCurrentControlIndex() + 1].isEnabled()) {
                j = this.getChildren()[this.getCurrentControlIndex()];
                j.setValue(j.createValue(parseFloat(c)), true);
                ++this.iCurrentControlIndex;
                this.setValue(j.createValue(parseFloat(c)), h);
                --this.iCurrentControlIndex
            }
            c = d.getValue().get()
        }
    }
    j = this.getChildren()[this.getCurrentControlIndex()];
    j.setValue(j.createValue(parseFloat(c)), true);
    this.syncControlElement()
}, syncControlElement:function () {
    var a = this.calculatePositionByValue(this.getChildren()[this.getCurrentControlIndex()].getValue());
    if (a == this.getCurrentControl().dPosition) {
        return
    }
    this.getCurrentControl().dPosition = a;
    this.updateControlElement();
    this.updateRanges();
    this.updateBounds()
}, updateControlElement:function () {
    var a = this.getCurrentControl();
    a.oElement.style.left = Math.round(a.dPosition) + "%";
    a.oValueElement.style.left = Math.round(a.dPosition) + "%";
    a.oValueElement.innerHTML = this.getChildren()[this.getCurrentControlIndex()].getValue().get().formatNumber()
}, updateRanges:function () {
    var a = this.getCurrentControlIndex(), b = this.getCurrentControl();
    this.moveRangeElement(b.oLeftRangeElement, a > 0 ? this.aControls[a - 1].dPosition : 0, b.dPosition);
    this.moveRangeElement(b.oRightRangeElement, b.dPosition, a < this.aControls.length - 1 ? this.aControls[a + 1].dPosition : 100)
}, moveRangeElement:function (b, c, a) {
    Common.Dom.setStyle(b, "left: " + Math.round(c) + "%;width: " + (Math.round(a) - Math.round(c)) + "%")
}, updateBounds:function () {
    var a = [], d = this.getChildren(), e = function (f, g) {
        return f.dValue == g
    };
    for (var c = 0, b; c < d.length; c++) {
        b = parseFloat(d[c].getValue().get());
        a.push(b);
        if (this.aControls[c].bSelected) {
            if (!this.aMarks.contains(b, e)) {
                Common.Class.remove(this.aControls[c].oValueElement, this.__self.CLASS_NAME_VALUE_ELEMENT_SELECTED);
                this.aControls[c].bSelected = false
            }
        } else {
            if (this.aMarks.contains(b, e)) {
                Common.Class.add(this.aControls[c].oValueElement, this.__self.CLASS_NAME_VALUE_ELEMENT_SELECTED);
                this.aControls[c].bSelected = true
            }
        }
    }
    for (var c = 0; c < this.aMarks.length; c++) {
        if (this.aMarks[c].bSelected) {
            if (!a.contains(this.aMarks[c].dValue)) {
                Common.Class.remove(this.aMarks[c].oElement, this.__self.CLASS_NAME_MARK_ELEMENT_SELECTED);
                this.aMarks[c].bSelected = false
            }
        } else {
            if (a.contains(this.aMarks[c].dValue)) {
                Common.Class.add(this.aMarks[c].oElement, this.__self.CLASS_NAME_MARK_ELEMENT_SELECTED);
                this.aMarks[c].bSelected = true
            }
        }
    }
}, next:function () {
    if (!this.isEnabled() || !this.getChildren()[this.getCurrentControlIndex()].isEnabled()) {
        return false
    }
    var a = this.getChildren()[this.getCurrentControlIndex()].getValue();
    this.setValue(new ZForms.Value.Number(parseFloat(a.get()) + parseFloat(this.findNextStepByValue(a))))
}, prev:function () {
    if (!this.isEnabled() || !this.getChildren()[this.getCurrentControlIndex()].isEnabled()) {
        return false
    }
    var a = this.getChildren()[this.getCurrentControlIndex()].getValue();
    this.setValue(new ZForms.Value.Number(parseFloat(a.get()) - parseFloat(this.findPrevStepByValue(a))))
}, updateContainerOffset:function () {
    this.oContainerOffset = Common.Dom.getAbsoluteCoords(this.oContainer)
}, calculateOffset:function (a) {
    return Common.Event.getAbsoluteCoords(a).iLeft - this.oContainerOffset.iLeft
}, calculatePositionByValue:function (b) {
    var c = this.findSlideRuleIndexByValue(b), d = this.getSlideRuleByIndex(c), a = this.getSlideRuleByIndex(c + 1);
    return(b.get() - d.dValue) / (a.dValue - d.dValue) * (a.dPercent - d.dPercent) + d.dPercent
}, calculateValueByOffset:function (c) {
    var e = this.calculatePercentByOffset(c);
    if (e > 100) {
        e = 100
    } else {
        if (e < 0) {
            e = 0
        }
    }
    var b = this.findSlideRuleIndexByPercent(e), d = this.getSlideRuleByIndex(b), a = this.getSlideRuleByIndex(b + 1);
    return new ZForms.Value.Number((e - this.aSlideRules[b].dPercent) / (a.dPercent - d.dPercent) * (a.dValue - d.dValue) + d.dValue)
}, calculatePercentByOffset:function (a) {
    return a / this.oContainer.offsetWidth * 100
}, findSlideRuleIndexByPercent:function (b) {
    if (b == 0) {
        return 0
    }
    for (var a = 0; a < this.aSlideRules.length; a++) {
        if (this.aSlideRules[a].dPercent >= b) {
            return a - 1
        }
    }
    return this.aSlideRules.length - 2
}, findSlideRuleIndexByValue:function (a) {
    if (a.get() == this.getMin()) {
        return 0
    }
    for (var b = 1; b < this.aSlideRules.length; b++) {
        if (this.aSlideRules[b].dValue >= a.get()) {
            return b - 1
        }
    }
    return this.aSlideRules.length - 2
}, findNextStepByValue:function (a) {
    if (a.get() == this.getMin()) {
        return this.aSlideRules[0].dStep
    }
    for (var b = 0; b < this.aSlideRules.length; b++) {
        if (this.aSlideRules[b].dValue == a.get()) {
            return this.aSlideRules[b].dStep
        } else {
            if (this.aSlideRules[b].dValue > a.get()) {
                return this.aSlideRules[b - 1].dStep
            }
        }
    }
    return this.aSlideRules[this.aSlideRules.length - 1].dStep
}, findPrevStepByValue:function (a) {
    if (a.get() == this.getMin()) {
        return this.aSlideRules[0].dStep
    }
    for (var b = 0; b < this.aSlideRules.length; b++) {
        if (this.aSlideRules[b].dValue >= a.get()) {
            return this.aSlideRules[b - 1].dStep
        }
    }
    return this.aSlideRules[this.aSlideRules.length - 1].dStep
}, getSlideRuleByIndex:function (a) {
    return this.aSlideRules[a]
}, disableControlByIndex:function (a) {
    Common.Class.add(this.aControls[a].oElement, this.__self.CLASS_NAME_CONTROL_ELEMENT_DISABLED);
    Common.Class.add(this.aControls[a].oValueElement, this.__self.CLASS_NAME_VALUE_ELEMENT_DISABLED)
}, enableControlByIndex:function (a) {
    Common.Class.remove(this.aControls[a].oElement, this.__self.CLASS_NAME_CONTROL_ELEMENT_DISABLED);
    Common.Class.remove(this.aControls[a].oValueElement, this.__self.CLASS_NAME_VALUE_ELEMENT_DISABLED)
}, destruct:function () {
    this.oContainer = null;
    this.oScaleElement = null;
    if (!this.isTemplate()) {
        for (i = 0; i < this.aMarks.length; i++) {
            this.aMarks[i].oElement = null
        }
        for (i = 0; i < this.aControls.length; i++) {
            this.aControls[i].oElement = null;
            this.aControls[i].oValueElement = null;
            this.aControls[i].oLeftRangeElement = null;
            this.aControls[i].oRightRangeElement = null
        }
    }
    this.__base()
}}, {CLASS_NAME_SLIDER:"zf-slider-horizontal", CLASS_NAME_SLIDER_SCALE:"zf-slider-scale", CLASS_NAME_CONTROL_ELEMENT:"zf-slider-control", CLASS_NAME_CONTROL_ELEMENT_SELECTED:"zf-slider-control-selected", CLASS_NAME_CONTROL_ELEMENT_DISABLED:"zf-slider-control-disabled", CLASS_NAME_VALUE_ELEMENT:"zf-slider-value", CLASS_NAME_VALUE_ELEMENT_SELECTED:"zf-slider-value-selected", CLASS_NAME_VALUE_ELEMENT_DISABLED:"zf-slider-value-disabled", CLASS_NAME_MARK_ELEMENT:"zf-slider-mark", CLASS_NAME_MARK_ELEMENT_SELECTED:"zf-slider-mark-selected", CLASS_NAME_RANGE_ELEMENT:"zf-slider-range", aAll:[], iActiveIndex:0, add:function (a) {
    if (!(a instanceof this)) {
        return
    }
    this.aAll.push(a);
    return this.aAll.length - 1
}, setActiveIndex:function (a) {
    this.iActiveIndex = a
}});
ZForms.Widget.Container.Slider.Vertical = ZForms.Widget.Container.Slider.inheritTo({setupMarkElementPosition:function (a, b) {
    a.style.bottom = b + "%"
}, updateControlElement:function () {
    var a = this.getCurrentControl();
    a.oElement.style.bottom = Math.round(a.dPosition) + "%";
    a.oValueElement.style.bottom = Math.round(a.dPosition) + "%";
    a.oValueElement.innerHTML = this.getChildren()[this.getCurrentControlIndex()].getValue().get().formatNumber()
}, moveRangeElement:function (b, c, a) {
    var d = Math.round(a) - Math.round(c);
    Common.Dom.setStyle(b, "bottom: " + Math.round(c) + "%;height: " + (d > 0 ? (b.parentNode.offsetHeight * d / 100 + "px;") : "0px;"))
}, calculateOffset:function (a) {
    return this.oContainerOffset.iTop + this.oContainer.offsetHeight - Common.Event.getAbsoluteCoords(a).iTop
}, calculatePercentByOffset:function (a) {
    return a / this.oContainer.offsetHeight * 100
}}, {CLASS_NAME_SLIDER:"zf-slider-vertical"});
ZForms.Widget.Button = ZForms.Widget.inheritTo({__constructor:function (b, c, a) {
    this.__base(b, c, a);
    this.fHandler = null;
    this.fDisableHandler = function (d) {
        Common.Event.cancel(d)
    }
}, hasValue:function () {
    return false
}, setHandler:function (a) {
    if (this.fHandler) {
        Common.Event.remove(this.oElement, this.__self.DOM_EVENT_TYPE_CLICK, this.fHandler)
    }
    this.fHandler = a;
    if (this.isEnabled()) {
        this.enable(false, true)
    }
}, enable:function (c, b) {
    var a = this.__base(c);
    if (!(a || b)) {
        return false
    }
    if ((b || a) && this.fHandler) {
        Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_CLICK, this.fHandler)
    }
    if (a) {
        Common.Event.remove([this.oElement, this.oClassElement], [this.__self.DOM_EVENT_TYPE_CLICK, this.__self.DOM_EVENT_TYPE_MOUSEDOWN, this.__self.DOM_EVENT_TYPE_SELECTSTART], this.fDisableHandler)
    }
    return a
}, disable:function (a) {
    if (!this.__base(a)) {
        return false
    }
    if (this.fHandler) {
        Common.Event.remove(this.oElement, this.__self.DOM_EVENT_TYPE_CLICK, this.fHandler)
    }
    Common.Event.add([this.oElement, this.oClassElement], [this.__self.DOM_EVENT_TYPE_CLICK, this.__self.DOM_EVENT_TYPE_MOUSEDOWN, this.__self.DOM_EVENT_TYPE_SELECTSTART], this.fDisableHandler);
    return true
}}, {CLASS_NAME_BUTTON:"zf-button"});
ZForms.Widget.Button.Submit = ZForms.Widget.Button.inheritTo({getDefaultOptions:function () {
    return Common.Object.extend(this.__base(), {bDisableOnSubmit:true}, true)
}, setForm:function (b) {
    this.__base(b);
    this.oForm.addSubmit(this);
    if (!this.oOptions.bDisableOnSubmit) {
        return
    }
    var a = this;
    this.setHandler(function () {
        a.oForm.setCurrentSubmit(a)
    })
}, prepareForSubmit:function () {
    if (this.oOptions.bDisableOnSubmit) {
        this.disable()
    }
    this.__base()
}, addDependence:function (a) {
}});
ZForms.Widget.Container.Form = ZForms.Widget.Container.inheritTo({__constructor:function (b, c, a) {
    this.__base(b, c, a);
    this.oForm = this;
    this.aWidgets = [];
    this.aWidgets[this.getId()] = this;
    this.aSubmits = [];
    this.oCurrentSubmit = null;
    this.oHiddenSubmitElement = null;
    this.iChangedCounter = 0;
    this.bReadyForSubmit = true;
    this.bSubmitted = false;
    this.addExtendedHandlers();
    ZForms.aForms[this.getId()] = this
}, getDefaultOptions:function () {
    return Common.Object.extend(this.__base(), {bUpdatableSubmit:true, bCheckForValid:true, bCheckForChanged:false, bPreventSubmit:false}, true)
}, addExtendedHandlers:function () {
    var a = this;
    Common.Event.add(this.oElement, this.__self.DOM_EVENT_TYPE_SUBMIT, function (b) {
        if (!a.checkForSubmit() || a.bSubmitted) {
            return Common.Event.cancel(b)
        }
        ZForms.notifyObservers(ZForms.EVENT_TYPE_ON_BEFORE_SUBMIT, a);
        if (a.oOptions.bPreventSubmit) {
            return Common.Event.cancel(b)
        }
        a.prepareForSubmit();
        a.bSubmitted = true
    });
    Common.Event.add(window, Common.Browser.isIE() ? this.__self.DOM_EVENT_TYPE_BEFOREUNLOAD : this.__self.DOM_EVENT_TYPE_UNLOAD, function () {
        a.destruct()
    })
}, checkForSubmit:function () {
    if (this.isReadyForSubmit()) {
        return true
    }
    this.getFirstErrorWidget().focus();
    this.addClass(this.__self.CLASS_NAME_SUBMITTED);
    return false
}, init:function () {
    var a = this;
    setTimeout(function () {
        a.addClass(a.__self.CLASS_NAME_INITED);
        ZForms.Widget.Container.prototype.init.call(a);
        a.updateSubmit(true)
    }, 0)
}, setForm:function (a) {
}, increaseChangedCounter:function () {
    this.iChangedCounter++
}, decreaseChangedCounter:function () {
    this.iChangedCounter--
}, isChanged:function () {
    return this.iChangedCounter > 0
}, addChild:function (a) {
    a.setForm(this);
    return this.__base(a)
}, addSubmit:function (a) {
    if (!(a instanceof ZForms.Widget.Button.Submit)) {
        return
    }
    this.aSubmits.push(a)
}, updateSubmit:function (a) {
    var b = this.isReadyForSubmit(true);
    if (!a && b == this.bReadyForSubmit) {
        return
    }
    this.bReadyForSubmit = b;
    if (this.oOptions.bUpdatableSubmit && this.aSubmits.length > 0) {
        if (b) {
            this.enableSubmit()
        } else {
            this.disableSubmit()
        }
    }
    ZForms.notifyObservers(ZForms.EVENT_TYPE_ON_READY_CHANGE, this, b)
}, enableSubmit:function () {
    for (var a = 0; a < this.aSubmits.length; a++) {
        this.aSubmits[a].enable()
    }
}, disableSubmit:function () {
    for (var a = 0; a < this.aSubmits.length; a++) {
        this.aSubmits[a].disable()
    }
}, addWidget:function (a) {
    this.aWidgets[a.getId()] = a
}, removeWidget:function (a) {
    delete this.aWidgets[a.getId()]
}, getWidgetById:function (a) {
    return this.aWidgets[a]
}, getWidgets:function () {
    return this.aWidgets
}, isReadyForSubmit:function (c) {
    if (!c) {
        return this.bReadyForSubmit
    }
    var a = this.aWidgets;
    for (var b in a) {
        if (!a.hasOwnProperty(b) || a[b] == this) {
            continue
        }
        if (!a[b].isReadyForSubmit()) {
            return false
        }
    }
    return !this.oOptions.bCheckForChanged || this.isChanged()
}, getFirstErrorWidget:function () {
    for (var a in this.aWidgets) {
        if (!this.aWidgets.hasOwnProperty(a)) {
            continue
        }
        oWidget = this.aWidgets[a];
        if (oWidget.isEnabled() && (oWidget.bRequired || (this.oOptions.bCheckForValid && !oWidget.bValid))) {
            return oWidget
        }
    }
}, reset:function () {
    this.oElement.reset()
}, prepareForSubmit:function () {
    this.__base();
    if (this.oHiddenSubmitElement) {
        this.oHiddenSubmitElement.parentNode.remove(this.oHiddenSubmitElement)
    }
    if (this.oCurrentSubmit && this.oCurrentSubmit.oOptions.bDisableOnSubmit) {
        this.oHiddenSubmitElement = this.oElement.appendChild(Common.Dom.createElement("input", {type:"hidden", name:this.oCurrentSubmit.oElement.name, value:this.oCurrentSubmit.oElement.value}));
        this.oCurrentSubmit = null
    }
}, setCurrentSubmit:function (a) {
    this.oCurrentSubmit = a
}}, {CLASS_NAME_INITED:"zf-inited", CLASS_NAME_SUBMITTED:"zf-submitted", DOM_EVENT_TYPE_SUBMIT:"submit"});
ZForms.Widget.Container.Multiplicator = ZForms.Widget.Container.inheritTo({__constructor:function (b, c, a) {
    this.oTemplate = null;
    this.sButtonAddId = a ? a.sButtonAddId : null;
    this.sButtonRemoveId = a ? a.sButtonRemoveId : null;
    this.sButtonUpId = a ? a.sButtonUpId : null;
    this.sButtonDownId = a ? a.sButtonDownId : null;
    this.sInitialChildrenHash = null;
    this.sLastProcessedChildrenHash = null;
    this.__base(b || document.createElement("div"), c, a)
}, getDefaultOptions:function () {
    return Common.Object.extend(this.__base(), {iMin:1, iMax:10, bNameHasPostfix:false}, true)
}, addChild:function (d, c) {
    var b = c > -1 ? c : this.aChildren.length, a = new ZForms.Multiplier(this, d), e = (b > 0 ? "_" + b : "");
    if (this.sButtonAddId) {
        a.addAddButton(ZForms.createButton(document.getElementById(this.sButtonAddId + e)))
    }
    if (this.sButtonRemoveId) {
        a.addRemoveButton(ZForms.createButton(document.getElementById(this.sButtonRemoveId + e)))
    }
    if (this.sButtonUpId) {
        a.addUpButton(ZForms.createButton(document.getElementById(this.sButtonUpId + e)))
    }
    if (this.sButtonDownId) {
        a.addDownButton(ZForms.createButton(document.getElementById(this.sButtonDownId + e)))
    }
    d.setMultiplier(a);
    this.updateChildIndex(d, 0, b);
    return this.__base(d, c)
}, addTemplate:function (a) {
    this.oTemplate = a;
    a.setMultiplier(new ZForms.Multiplier(this, a));
    if (this.oForm) {
        a.setForm(this.oForm)
    }
    return a
}, normalizeTemplateAttributes:function (b) {
    var a = b.oClassElement.getElementsByTagName("script");
    while (a.length > 0) {
        a[0].parentNode.removeChild(a[0])
    }
    this.replacePostfixAtElement(b.oClassElement, this.oOptions.iMax + 1);
    b.setId(b.oElement.id)
}, calculateCurrentChildrenHash:function () {
    var c = "";
    for (var b = 0, a = this.aChildren.length; b < a; b++) {
        c += Common.Dom.getUniqueId(this.aChildren[b].oElement)
    }
    return c
}, processChildrenHashChanged:function () {
    var a = this.calculateCurrentChildrenHash();
    if (this.sInitialChildrenHash == a) {
        if (this.sLastProcessedChildrenHash != this.sInitialChildrenHash) {
            this.oForm.decreaseChangedCounter();
            this.oForm.updateSubmit()
        }
    } else {
        if (this.sLastProcessedChildrenHash == this.sInitialChildrenHash) {
            this.oForm.increaseChangedCounter();
            this.oForm.updateSubmit()
        }
    }
    this.sLastProcessedChildrenHash = a
}, init:function () {
    this.__base();
    if (!this.oTemplate) {
        ZForms.throwException("template not found")
    }
    for (var a = 0; a < this.aChildren.length; a++) {
        this.aChildren[a].addId(a)
    }
    this.oTemplate.hide();
    this.oTemplate.disable();
    this.oTemplate.addId(this.oOptions.iMax + 1);
    this.normalizeTemplateAttributes(this.oTemplate);
    this.updateMultipliers();
    this.sInitialChildrenHash = this.calculateCurrentChildrenHash();
    this.sLastProcessedChildrenHash = this.sInitialChildrenHash
}, updateMultipliers:function () {
    for (var a = 0; a < this.aChildren.length; a++) {
        this.aChildren[a].getMultiplier().updateState(this.aChildren.length < this.oOptions.iMax, this.aChildren.length > this.oOptions.iMin, a > 0, a < this.aChildren.length - 1)
    }
}, add:function (e) {
    var d = this.aChildren.indexOf(e) + 1, b = this.oTemplate.oClassElement.cloneNode(true);
    this.increaseChildrenPostfix(d);
    this.removePostfixFromElement(b);
    this.addPostfixToElement(b, d);
    if (e.oClassElement.nextSibling) {
        e.oClassElement.parentNode.insertBefore(b, e.oClassElement.nextSibling)
    } else {
        e.oClassElement.parentNode.appendChild(b)
    }
    var c = this.oTemplate.clone(document.getElementById(this.oTemplate.oElement.id.match(this.__self.REG_EXP_REPLACE)[1] + "_" + d), document.getElementById(this.oTemplate.oClassElement.id.match(this.__self.REG_EXP_REPLACE)[1] + "_" + d), d);
    var a = this.oTemplate.getMultiplier();
    if (!this.sButtonAddId && a.oAddButton) {
        this.sButtonAddId = a.oAddButton.oElement.id.match(this.__self.REG_EXP_REPLACE)[1]
    }
    if (!this.sButtonRemoveId && a.oRemoveButton) {
        this.sButtonRemoveId = a.oRemoveButton.oElement.id.match(this.__self.REG_EXP_REPLACE)[1]
    }
    if (!this.sButtonUpId && a.oUpButton) {
        this.sButtonUpId = a.oUpButton.oElement.id.match(this.__self.REG_EXP_REPLACE)[1]
    }
    if (!this.sButtonDownId && a.oDownButton) {
        this.sButtonDownId = a.oDownButton.oElement.id.match(this.__self.REG_EXP_REPLACE)[1]
    }
    this.addChild(c, d);
    c.disable();
    c.enable();
    c.show();
    this.updateMultipliers();
    this.addTemplateDependencies(this.oTemplate, c, c);
    c.afterClone();
    this.repaintFix();
    this.processChildrenHashChanged()
}, addTemplateDependencies:function (c, a, d) {
    this.addDependenciesFrom(c, a, d);
    this.addDependenciesTo(c, a, d);
    if (c instanceof ZForms.Widget.Container) {
        for (var b = 0; b < c.aChildren.length; b++) {
            this.addTemplateDependencies(c.aChildren[b], a.aChildren[b], d)
        }
    }
}, addDependenciesFrom:function (e, c, g) {
    for (var d = 0, a = e.getDependencies(), b, f; d < a.length; d++) {
        b = this.findCorrespondingWidgetByTemplate(a[d].getFrom(), this.oTemplate, g) || a[d].getFrom();
        f = a[d].clone(b);
        if (f instanceof ZForms.Dependence.Function) {
            f.getFunction().mArgument = this.findCorrespondingWidgetByTemplate(a[d].getFunction().mArgument, this.oTemplate, g) || a[d].getFunction().mArgument;
            f.getFunction().oWidget = this.findCorrespondingWidgetByTemplate(a[d].getFunction().oWidget, this.oTemplate, g) || a[d].getFunction().oWidget;
            f.getFunction().iType = a[d].getFunction().iType;
            f.getFunction().sFunctionName = a[d].getFunction().sFunctionName;
            f.getFunction().oOptions = a[d].getFunction().oOptions
        }
        c.addDependence(f);
        b.processEvents(true, true)
    }
}, addDependenciesTo:function (e, c, f) {
    for (var d = 0, a; d < e.aObservers.length; d++) {
        if (this.findCorrespondingWidgetByTemplate(e.aObservers[d], this.oTemplate, f)) {
            continue
        }
        a = e.aObservers[d].getDependencies();
        for (var b = 0; b < a.length; b++) {
            if (a[b].getFrom() == e) {
                e.aObservers[d].addDependence(a[b].clone(c))
            }
        }
    }
}, findCorrespondingWidgetByTemplate:function (a, d, b) {
    if (d == a) {
        return b
    }
    if (d instanceof ZForms.Widget.Container) {
        for (var c = 0, e; c < d.aChildren.length; c++) {
            e = this.findCorrespondingWidgetByTemplate(a, d.aChildren[c], b.aChildren[c]);
            if (e) {
                return e
            }
        }
    }
}, remove:function (b) {
    var a = this.aChildren.indexOf(b);
    b.oClassElement.parentNode.removeChild(b.oClassElement);
    this.decreaseChildrenPostfix(a + 1);
    this.removeChild(b);
    this.processEvents(true);
    this.updateMultipliers();
    this.repaintFix();
    this.processChildrenHashChanged()
}, up:function (b) {
    var a = this.aChildren.indexOf(b);
    this.aChildren[a - 1].oClassElement.parentNode.insertBefore(b.oClassElement.parentNode.removeChild(b.oClassElement), this.aChildren[a - 1].oClassElement);
    this.aChildren.remove(b);
    this.aChildren.splice(a - 1, 0, b);
    if (a - 1 > 0) {
        this.replacePostfixAtElement(this.aChildren[a].oClassElement, a)
    } else {
        this.addPostfixToElement(this.aChildren[a].oClassElement, a)
    }
    this.updateChildIndex(this.aChildren[a - 1], a, a - 1);
    this.replacePostfixAtElement(this.aChildren[a - 1].oClassElement, a - 1);
    this.aChildren[a - 1].updateElements(a - 1);
    this.updateChildIndex(this.aChildren[a], a - 1, a);
    this.aChildren[a].updateElements(a);
    this.updateMultipliers();
    this.repaintFix();
    this.processChildrenHashChanged()
}, down:function (b) {
    var a = this.aChildren.indexOf(b);
    if (this.aChildren[a + 2]) {
        this.aChildren[a + 2].oClassElement.parentNode.insertBefore(b.oClassElement.parentNode.removeChild(b.oClassElement), this.aChildren[a + 2].oClassElement)
    } else {
        this.aChildren[a + 1].oClassElement.parentNode.insertBefore(b.oClassElement.parentNode.removeChild(b.oClassElement), this.oTemplate.oClassElement)
    }
    this.aChildren.remove(b);
    this.aChildren.splice(a + 1, 0, b);
    this.updateChildIndex(this.aChildren[a], a + 1, a);
    this.replacePostfixAtElement(this.aChildren[a].oClassElement, a);
    this.aChildren[a].updateElements(a);
    this.updateChildIndex(this.aChildren[a + 1], a, a + 1);
    if (a > 0) {
        this.replacePostfixAtElement(this.aChildren[a + 1].oClassElement, a + 1)
    } else {
        this.addPostfixToElement(this.aChildren[a + 1].oClassElement, a + 1)
    }
    this.aChildren[a + 1].updateElements(a + 1);
    this.updateMultipliers();
    this.repaintFix();
    this.processChildrenHashChanged()
}, updateChildIndex:function (a, c, b) {
    a.replaceClass(this.__self.CHILD_INDEX_CLASS_NAME_PREFIX + c, this.__self.CHILD_INDEX_CLASS_NAME_PREFIX + b)
}, increaseChildrenPostfix:function (a) {
    for (var b = this.aChildren.length - 1; b >= a; b--) {
        this.replacePostfixAtElement(this.aChildren[b].oClassElement, b + 1);
        this.aChildren[b].updateElements(b + 1);
        this.updateChildIndex(this.aChildren[b], b, b + 1)
    }
}, decreaseChildrenPostfix:function (a) {
    for (var b = a; b < this.aChildren.length; b++) {
        this.replacePostfixAtElement(this.aChildren[b].oClassElement, b - 1);
        this.aChildren[b].updateElements(b - 1);
        this.updateChildIndex(this.aChildren[b], b, b - 1)
    }
}, replacePostfixAtElement:function (c, a) {
    for (var b = 0; b < c.childNodes.length; b++) {
        this.replacePostfixAtElement(c.childNodes[b], a)
    }
    this.replacePostfixAtNode(c, a)
}, replacePostfixAtNode:function (b, a) {
    if (b.id) {
        b.id = b.id.replace(this.__self.REG_EXP_REPLACE, "$1" + (a > 0 ? "_" + a : ""))
    }
    if (b.htmlFor) {
        b.htmlFor = b.htmlFor.replace(this.__self.REG_EXP_REPLACE, "$1" + (a > 0 ? "_" + a : ""))
    }
    if (this.oOptions.bNameHasPostfix && b.name) {
        b.name = b.name.replace(this.__self.REG_EXP_REPLACE, "$1" + (a > 0 ? "_" + a : "") + "$2");
        this.fixNode(b)
    }
}, removePostfixFromElement:function (b) {
    for (var a = 0; a < b.childNodes.length; a++) {
        this.removePostfixFromElement(b.childNodes[a])
    }
    this.removePostfixFromNode(b)
}, removePostfixFromNode:function (a) {
    if (this.oOptions.bNameHasPostfix && a.name) {
        a.name = a.name.replace(this.__self.REG_EXP_REPLACE, "$1$2")
    }
    if (a.id) {
        a.id = a.id.replace(this.__self.REG_EXP_REPLACE, "$1")
    }
    if (a.htmlFor) {
        a.htmlFor = a.htmlFor.replace(this.__self.REG_EXP_REPLACE, "$1")
    }
}, addPostfixToElement:function (c, a) {
    for (var b = 0; b < c.childNodes.length; b++) {
        this.addPostfixToElement(c.childNodes[b], a)
    }
    this.addPostfixToNode(c, a)
}, addPostfixToNode:function (b, a) {
    if (b.id) {
        b.id += "_" + a
    }
    if (b.htmlFor) {
        b.htmlFor += "_" + a
    }
    if (this.oOptions.bNameHasPostfix && b.name) {
        b.name = b.name.replace(/^([^\[]+)(\[\])?$/, "$1_" + a + "$2");
        this.fixNode(b)
    }
}, fixNode:function (c) {
    var a = c.type.toLowerCase();
    if (!Common.Browser.isIE() || !(a == "text" || a == "radio" || a == "checkbox")) {
        return
    }
    var b = {type:c.type, name:c.name, id:c.id, "class":c.className, size:c.size, maxlength:c.maxLength, value:c.value, style:c.style.cssText};
    if (c.checked) {
        b.checked = "checked"
    }
    c.parentNode.replaceChild(Common.Dom.createElement("input", b), c).outerHTML = ""
}, destruct:function () {
    if (this.oTemplate) {
        this.oTemplate.destruct()
    }
    this.__base()
}, repaintFix:function () {
    if (document.compatMode) {
        return
    }
    document.body.className += ""
}}, {POSTFIX_ID:"_multiplicator", REG_EXP_REPLACE:/^(.+)_\d+(\[\])?$/, CHILD_INDEX_CLASS_NAME_PREFIX:"zf-child_"});
ZForms.Multiplier = Abstract.inheritTo({__constructor:function (b, a) {
    this.oMultiplicator = b;
    this.oWidget = a;
    this.bCanAdd = true;
    this.bCanRemove = true;
    this.bCanUp = true;
    this.bCanDown = true;
    this.oAddButton = null;
    this.oRemoveButton = null;
    this.oUpButton = null;
    this.oDownButton = null;
    this.bDisabledByOuter = false
}, addAddButton:function (b) {
    this.oAddButton = b;
    var a = this;
    b.setHandler(function () {
        a.oMultiplicator.add(a.oWidget);
        return false
    })
}, addRemoveButton:function (b) {
    this.oRemoveButton = b;
    var a = this;
    b.setHandler(function () {
        a.oMultiplicator.remove(a.oWidget);
        return false
    })
}, addUpButton:function (b) {
    this.oUpButton = b;
    var a = this;
    b.setHandler(function () {
        a.oMultiplicator.up(a.oWidget);
        return false
    })
}, addDownButton:function (b) {
    this.oDownButton = b;
    var a = this;
    b.setHandler(function () {
        a.oMultiplicator.down(a.oWidget);
        return false
    })
}, enableByOuter:function () {
    this.bDisabledByOuter = false;
    if (this.bCanAdd) {
        this.enableAdd()
    }
    if (this.bCanRemove) {
        this.enableRemove()
    }
}, disableByOuter:function () {
    this.bDisabledByOuter = true;
    if (this.oAddButton) {
        this.oAddButton.disable()
    }
    if (this.oRemoveButton) {
        this.oRemoveButton.disable()
    }
}, enableAdd:function () {
    this.bCanAdd = true;
    if (this.bDisabledByOuter) {
        return
    }
    if (this.oAddButton) {
        this.oAddButton.enable()
    }
}, disableAdd:function () {
    this.bCanAdd = false;
    if (this.oAddButton) {
        this.oAddButton.disable()
    }
}, enableRemove:function () {
    this.bCanRemove = true;
    if (this.bDisabledByOuter) {
        return
    }
    if (this.oRemoveButton) {
        this.oRemoveButton.enable()
    }
}, disableRemove:function () {
    this.bCanRemove = false;
    if (this.oRemoveButton) {
        this.oRemoveButton.disable()
    }
}, enableUp:function () {
    this.bCanUp = true;
    if (this.bDisabledByOuter) {
        return
    }
    if (this.oUpButton) {
        this.oUpButton.enable()
    }
}, disableUp:function () {
    this.bCanUp = false;
    if (this.oUpButton) {
        this.oUpButton.disable()
    }
}, enableDown:function () {
    this.bCanDown = true;
    if (this.bDisabledByOuter) {
        return
    }
    if (this.oDownButton) {
        this.oDownButton.enable()
    }
}, disableDown:function () {
    this.bCanDown = false;
    if (this.oDownButton) {
        this.oDownButton.disable()
    }
}, updateState:function (a, b, c, d) {
    if (a) {
        this.enableAdd()
    } else {
        this.disableAdd()
    }
    if (b) {
        this.enableRemove()
    } else {
        this.disableRemove()
    }
    if (c) {
        this.enableUp()
    } else {
        this.disableUp()
    }
    if (d) {
        this.enableDown()
    } else {
        this.disableDown()
    }
}, init:function () {
    if (this.oAddButton) {
        this.oAddButton.init()
    }
    if (this.oRemoveButton) {
        this.oRemoveButton.init()
    }
    if (this.oUpButton) {
        this.oUpButton.init()
    }
    if (this.oDownButton) {
        this.oDownButton.init()
    }
}, addId:function (a) {
    if (this.oAddButton) {
        this.oAddButton.addId(a)
    }
    if (this.oRemoveButton) {
        this.oRemoveButton.addId(a)
    }
    if (this.oUpButton) {
        this.oUpButton.addId(a)
    }
    if (this.oDownButton) {
        this.oDownButton.addId(a)
    }
}, destruct:function () {
    if (this.oAddButton) {
        this.oAddButton.destruct()
    }
    if (this.oRemoveButton) {
        this.oRemoveButton.destruct()
    }
    if (this.oUpButton) {
        this.oUpButton.destruct()
    }
    if (this.oDownButton) {
        this.oDownButton.destruct()
    }
}});
ZForms.Dependence = Abstract.inheritTo({__constructor:function (d, a, c, b, e) {
    this.iType = d;
    this.oFrom = a;
    this.rPattern = c;
    this.iLogic = b || this.__self.LOGIC_OR;
    this.bInverse = e || false
}, check:function () {
    if (this.oFrom.isTemplate()) {
        return true
    }
    var a = this.oFrom.getValue().match(this.rPattern);
    return this.isInverse() ? !a : a
}, getType:function () {
    return this.iType
}, getFrom:function () {
    return this.oFrom
}, getPattern:function () {
    return this.rPattern
}, getLogic:function () {
    return this.iLogic
}, isInverse:function () {
    return this.bInverse
}, clone:function (a) {
    return new this.__self(this.getType(), a, this.getPattern(), this.getLogic(), this.isInverse())
}, getResult:function () {
}}, {TYPE_REQUIRED:1, TYPE_VALID:2, TYPE_ENABLED:3, TYPE_OPTIONS:4, TYPE_CLASS:5, TYPE_CHECK:6, LOGIC_OR:1, LOGIC_AND:2, COMPARE_FUNCTIONS:{eq:"isEqual", gt:"isGreater", gte:"isGreaterOrEqual", lt:"isLess", lte:"isLessOrEqual"}});
ZForms.Dependence.Enabled = ZForms.Dependence.inheritTo({__constructor:function (a, d, c, e, b) {
    this.__base(this.__self.TYPE_ENABLED, a, d, c, e);
    this.bCheckResult = false;
    this.bFocusOnEnable = b
}, check:function () {
    if (this.oFrom.isTemplate()) {
        return true
    }
    this.bCheckResult = this.__base();
    return this.bCheckResult
}, getResult:function () {
    if (!this.bFocusOnEnable) {
        return
    }
    return{bFocusOnEnable:this.bCheckResult}
}});
ZForms.Dependence.Valid = ZForms.Dependence.inheritTo({__constructor:function (c, e, d, f, b, a) {
    this.__base(this.__self.TYPE_VALID, c, e, d, f);
    this.bCheckResult = false;
    this.sClassName = b;
    this.bCheckForEmpty = a
}, check:function () {
    if (this.oFrom.isTemplate() || (!this.bCheckForEmpty && this.oFrom.getValue().isEmpty())) {
        return true
    }
    this.bCheckResult = this.__base();
    return this.bCheckResult
}, getResult:function () {
    if (!this.sClassName) {
        return
    }
    return{bAdd:!this.bCheckResult, sClassName:this.sClassName}
}, clone:function (a) {
    return new this.__self(a, this.getPattern(), this.getLogic(), this.isInverse(), this.sClassName, this.bCheckForEmpty)
}});
ZForms.Dependence.Options = ZForms.Dependence.inheritTo({__constructor:function (d, a, c, b, e) {
    this.__base(d, a, null, b, e);
    this.aPatterns = c;
    this.aResult = []
}, getPatterns:function () {
    return this.aPatterns
}, check:function () {
    if (this.oFrom.isTemplate()) {
        return true
    }
    this.aResult = [];
    var c = this.oFrom.getValue(), b = false;
    for (var a = 0; a < this.aPatterns.length; a++) {
        b = c.match(this.aPatterns[a].rSource);
        if (this.bInverse ? !b : b) {
            this.aResult.push(this.aPatterns[a].rDestination)
        }
    }
    return true
}, getResult:function () {
    return this.aResult
}});
ZForms.Dependence.Required = ZForms.Dependence.inheritTo({__constructor:function (a, d, c, e, b) {
    this.__base(this.__self.TYPE_REQUIRED, a, d, c, e);
    this.iMin = b || 1;
    if (!(this.getFrom() instanceof ZForms.Widget.Container)) {
        this.iMin = 1
    }
}, getMin:function () {
    return this.iMin
}, check:function () {
    if (this.oFrom.isTemplate()) {
        return true
    }
    var f = 0, b = false, g = true, a = false;
    if (this.oFrom instanceof ZForms.Widget.Container.Group) {
        for (var e = 0; e < this.oFrom.aChildren.length; e++) {
            if (this.oFrom.aChildren[e].isChecked()) {
                f++
            }
        }
    } else {
        if (this.oFrom instanceof ZForms.Widget.Container && !(this.oFrom instanceof ZForms.Widget.Container.Date)) {
            g = false;
            for (var e = 0; e < this.oFrom.aChildren.length; e++) {
                if (this.oFrom.aChildren[e].isEnabled()) {
                    g = true
                } else {
                    continue
                }
                if (this.oFrom.aChildren[e] instanceof ZForms.Widget.Container && !(this.oFrom.aChildren[e] instanceof ZForms.Widget.Container.Date)) {
                    if (this.oFrom.aChildren[e].isRequired()) {
                        b = true
                    } else {
                        var d = 0;
                        if (this.oFrom.aChildren[e] instanceof ZForms.Widget.Container.Group) {
                            for (var c = 0; c < this.oFrom.aChildren[e].aChildren.length; c++) {
                                if (this.oFrom.aChildren[e].aChildren[c].isChecked()) {
                                    d++
                                }
                            }
                        } else {
                            d = this.oFrom.aChildren[e].getCountChildrenByPattern(this.rPattern)
                        }
                        if (this.oFrom.aChildren[e] instanceof ZForms.Widget.Container.Multiplicator) {
                            f += d
                        } else {
                            if (d > 0) {
                                f++
                            }
                        }
                    }
                } else {
                    if (this.oFrom.aChildren[e].isRequired()) {
                        b = true
                    } else {
                        if (this.oFrom.aChildren[e].getValue().match(/\S+/)) {
                            f++
                        }
                    }
                }
            }
        } else {
            if (this.oFrom.getValue().match(this.rPattern)) {
                f++
            }
        }
    }
    a = !b && (f >= this.iMin || !g);
    return this.isInverse() ? !a : a
}, clone:function (a) {
    return new this.__self(a, this.getPattern(), this.getLogic(), this.isInverse(), this.getMin())
}});
ZForms.Dependence.Class = ZForms.Dependence.inheritTo({__constructor:function (a, c, b) {
    this.__base(this.__self.TYPE_CLASS, a, null, b, false);
    this.aPatternToClasses = c;
    this.aResult = []
}, getPatternToClasses:function () {
    return this.aPatternToClasses
}, check:function () {
    if (this.oFrom.isTemplate()) {
        return true
    }
    this.aResult = [];
    var b = this.oFrom.getValue(), a = 0, c;
    while (c = this.aPatternToClasses[a++]) {
        this.aResult.push({sClassName:c.sClassName, bMatched:b.match(c.rPattern) ? !c.bInverse : c.bInverse})
    }
    return this.aResult.length > 0
}, clone:function (a) {
    return new this.__self(a, this.getPatternToClasses(), this.getLogic())
}, getResult:function () {
    return this.aResult
}});
ZForms.Dependence.Function = ZForms.Dependence.inheritTo({__constructor:function (c, a, e, b, d) {
    this.__base(c, a, null, b, d);
    this.fFunction = e;
    this.mResult = null
}, getFunction:function () {
    return this.fFunction
}, check:function () {
    if (this.oFrom.isTemplate()) {
        return true
    }
    this.mResult = null;
    var a = this.fFunction(this.oFrom, this);
    return this.isInverse() ? !a : a
}, setResult:function (a) {
    this.mResult = a
}, getResult:function () {
    return this.mResult
}, clone:function (oFrom) {
    eval("var fClonedFunction = " + this.getFunction().toString());
    return new this.__self(this.getType(), oFrom, fClonedFunction, this.getLogic(), this.isInverse())
}});
ZForms.DependenceGroup = Abstract.inheritTo({__constructor:function (a) {
    this.iType = a;
    this.aDependencies = []
}, getType:function () {
    return this.iType
}, addDependence:function (a) {
    this.aDependencies.push(a)
}, removeDependence:function (a) {
    this.aDependencies.remove(a)
}, getDependencies:function () {
    return this.aDependencies
}, check:function () {
    var a = this.aDependencies.length == 0, d = false;
    for (var c = 0, b = false; c < this.aDependencies.length; c++) {
        d = this.aDependencies[c].check();
        if (b) {
            continue
        }
        if (d && this.aDependencies[c].getLogic() == ZForms.Dependence.LOGIC_OR) {
            a = true;
            if (!(this.getType() == ZForms.Dependence.TYPE_CLASS || this.getType() == ZForms.Dependence.TYPE_OPTIONS)) {
                break
            }
        } else {
            if (!d && this.aDependencies[c].getLogic() == ZForms.Dependence.LOGIC_AND) {
                a = false;
                b = true;
                if (this.getType() != ZForms.Dependence.TYPE_VALID) {
                    break
                }
            } else {
                a = d
            }
        }
    }
    return a
}, getResult:function () {
    for (var b = 0, c = [], a; b < this.aDependencies.length; b++) {
        c.push(this.aDependencies[b].getResult())
    }
    return c
}});
ZForms.DependenceProcessor = Abstract.inheritTo({__constructor:function (a) {
    this.oWidget = a;
    this.aDependenceGroups = [];
    this.aCheckingOrder = [ZForms.Dependence.TYPE_ENABLED, ZForms.Dependence.TYPE_VALID, ZForms.Dependence.TYPE_REQUIRED, ZForms.Dependence.TYPE_OPTIONS, ZForms.Dependence.TYPE_CHECK, ZForms.Dependence.TYPE_CLASS]
}, addDependence:function (a) {
    if (!this.hasDependenciesByType(a.getType())) {
        this.aDependenceGroups[a.getType()] = new ZForms.DependenceGroup(a.getType())
    }
    this.aDependenceGroups[a.getType()].addDependence(a)
}, removeDependence:function (a) {
    this.aDependenceGroups[a.getType()].removeDependence(a)
}, getDependencies:function () {
    var b = [];
    for (var a = 0; a < this.aCheckingOrder.length; a++) {
        if (!this.hasDependenciesByType(this.aCheckingOrder[a])) {
            continue
        }
        b = b.concat(this.aDependenceGroups[this.aCheckingOrder[a]].getDependencies())
    }
    return b
}, hasDependenciesByType:function (a) {
    return this.aDependenceGroups[a] && this.aDependenceGroups[a].getDependencies().length > 0
}, process:function () {
    if (this.oWidget.isTemplate()) {
        return
    }
    for (var a = 0; a < this.aCheckingOrder.length; a++) {
        this.dispatchProcessDependencies(this.aCheckingOrder[a])
    }
}, dispatchProcessDependencies:function (a) {
    if (!this.hasDependenciesByType(a)) {
        return
    }
    switch (a) {
        case ZForms.Dependence.TYPE_ENABLED:
            this.processEnableDependencies();
            break;
        case ZForms.Dependence.TYPE_VALID:
            this.processValidDependencies();
            break;
        case ZForms.Dependence.TYPE_REQUIRED:
            this.processRequiredDependencies();
            break;
        case ZForms.Dependence.TYPE_OPTIONS:
        case ZForms.Dependence.TYPE_CHECK:
            this.processOptionsDependencies(a);
            break;
        case ZForms.Dependence.TYPE_CLASS:
            this.processClassDependencies();
            break;
        default:
            break
    }
}, processEnableDependencies:function () {
    var c = this.aDependenceGroups[ZForms.Dependence.TYPE_ENABLED].check(), d = this.aDependenceGroups[ZForms.Dependence.TYPE_ENABLED].getResult();
    if (c) {
        this.oWidget.enable()
    } else {
        this.oWidget.disable()
    }
    if (!this.oWidget.isInited()) {
        return
    }
    var b, a = 0;
    while (b = d[a++]) {
        if (b.bFocusOnEnable) {
            return this.oWidget.focus()
        }
    }
}, processValidDependencies:function () {
    var b = this.aDependenceGroups[ZForms.Dependence.TYPE_VALID].check(), c = this.aDependenceGroups[ZForms.Dependence.TYPE_VALID].getResult(), a = 0;
    if (b) {
        this.oWidget.setValid()
    } else {
        this.oWidget.setInvalid()
    }
    while (a < c.length) {
        if (c[a] && c[a].sClassName) {
            this.oWidget[(c[a].bAdd && !b ? "add" : "remove") + "Class"](c[a].sClassName)
        }
        ++a
    }
}, processRequiredDependencies:function () {
    if (this.aDependenceGroups[ZForms.Dependence.TYPE_REQUIRED].check() && this.oWidget.isValid()) {
        this.oWidget.unsetRequired()
    } else {
        this.oWidget.setRequired()
    }
}, processOptionsDependencies:function (c) {
    var a = this.aDependenceGroups[c].check(), b = this.aDependenceGroups[c].getResult();
    this.oWidget.enableOptionsByValue(b, this.aDependenceGroups[c].getDependencies()[0].getLogic() == ZForms.Dependence.LOGIC_OR, c == ZForms.Dependence.TYPE_CHECK)
}, processClassDependencies:function () {
    var c = this.aDependenceGroups[ZForms.Dependence.TYPE_CLASS].check(), e = this.aDependenceGroups[ZForms.Dependence.TYPE_CLASS].getResult(), a = this.aDependenceGroups[ZForms.Dependence.TYPE_CLASS].getDependencies()[0].getLogic() == ZForms.Dependence.LOGIC_AND, d = [];
    for (var b = 0; b < e.length; b++) {
        d = this.joinClassGroup(d, e[b], a)
    }
    if (c && d.length == 0) {
        return
    }
    for (var b = 0; b < d.length; b++) {
        if (d[b].bMatched) {
            this.oWidget.addClass(d[b].sClassName)
        } else {
            this.oWidget.removeClass(d[b].sClassName)
        }
    }
}, joinClassGroup:function (f, e, b) {
    if (f.length == 0) {
        return e
    }
    for (var d = 0, c = f.length; d < c; d++) {
        for (var a = 0; a < e.length; a++) {
            if (f[d].sClassName == e[a].sClassName) {
                if ((!b && e[a].bMatched) || (b && !e[a].bMatched)) {
                    f[d] = e[a]
                } else {
                    e[a] = f[d]
                }
            } else {
                if (!f.contains(e[a])) {
                    f[f.length] = e[a]
                }
            }
        }
    }
    return f
}});
ZForms.Calendar = Abstract.inheritTo({__constructor:function (a) {
    this.oWidget = a;
    this.oPickerButton = ZForms.createButton(a.oOptions.oPickerOpenerElement);
    this.oElement = Common.Dom.createElement("table", {"class":this.__self.CLASS_NAME_CALENDAR + " " + this.__self.CLASS_NAME_HIDDEN}).appendChild(Common.Dom.createElement("tbody"));
    this.oYearTitleElement = Common.Dom.createElement("span", {"class":this.__self.CLASS_NAME_TITLE});
    this.oMonthTitleElement = Common.Dom.createElement("span", {"class":this.__self.CLASS_NAME_TITLE});
    this.oDate = new Date();
    this.oDateNow = new Date();
    this.bShowed = false;
    this.fClickHandler = null;
    this.fMouseHandler = null;
    this.init()
}, init:function () {
    var j = this.oElement.parentNode.insertBefore(document.createElement("thead"), this.oElement), k = j.appendChild(document.createElement("tr")).appendChild(Common.Dom.createElement("th", {colspan:7})), a = k.appendChild(Common.Dom.createElement("input", {type:"button", value:"←", "class":this.__self.CLASS_NAME_ARROW_PREV + " " + ZForms.Widget.Button.CLASS_NAME_BUTTON})), h = k.appendChild(Common.Dom.createElement("input", {type:"button", value:"→", "class":this.__self.CLASS_NAME_ARROW_NEXT + " " + ZForms.Widget.Button.CLASS_NAME_BUTTON})), g = j.appendChild(document.createElement("tr")).appendChild(Common.Dom.createElement("th", {colspan:7})), e = g.appendChild(Common.Dom.createElement("input", {type:"button", value:"←", "class":this.__self.CLASS_NAME_ARROW_PREV + " " + ZForms.Widget.Button.CLASS_NAME_BUTTON})), b = g.appendChild(Common.Dom.createElement("input", {type:"button", value:"→", "class":this.__self.CLASS_NAME_ARROW_NEXT + " " + ZForms.Widget.Button.CLASS_NAME_BUTTON})), f = j.appendChild(document.createElement("tr"));
    k.appendChild(this.oYearTitleElement);
    g.appendChild(this.oMonthTitleElement);
    for (var c = 0; c < 7; c++) {
        f.appendChild(Common.Dom.createElement("th", {"class":c > 4 ? this.__self.CLASS_NAME_WEEKEND : null}, ZForms.Resources.getDaysOfWeek()[c]))
    }
    var d = this;
    this.oPickerButton.setHandler(function () {
        if (d.isShowed()) {
            d.hide()
        } else {
            var l = d.oWidget.getValue();
            if (d.oWidget.oOptions.bWithTime && l.isEmpty() && !d.oWidget.oYearInput.getValue().isEmpty()) {
                d.setDate(new Date(d.oWidget.oYearInput.getValue().get(), d.oWidget.oMonthInput.getValue().get(), d.oWidget.oDayInput.getValue().get()))
            } else {
                if (!l.isEmpty()) {
                    d.setDate(new Date(l.getYear(), l.getMonth() - 1, l.getDay()))
                }
            }
            d.show()
        }
    });
    Common.Event.add(this.oElement.parentNode, "click", function (l) {
        Common.Event.cancel(l)
    });
    Common.Event.add(document, "click", function (l) {
        if (Common.Event.normalize(l).target != d.oPickerButton.oElement) {
            d.hide()
        }
    });
    Common.Event.add(a, "click", function () {
        d.setPrevYear()
    });
    Common.Event.add(h, "click", function () {
        d.setNextYear()
    });
    Common.Event.add(e, "click", function () {
        d.setPrevMonth()
    });
    Common.Event.add(b, "click", function () {
        d.setNextMonth()
    });
    this.oPickerButton.oElement.parentNode.appendChild(this.oElement.parentNode);
    this.fClickHandler = function (n) {
        d.hide();
        var m = Common.Event.normalize(n).target, l = parseInt(m.innerHTML, 10);
        d.setDate(new Date(d.oDate.getFullYear(), d.oDate.getMonth() + (Common.Class.match(m, d.__self.CLASS_NAME_ADD) ? (l > 15 ? -1 : 1) : 0), m.innerHTML));
        if (d.oWidget.oOptions.bWithTime) {
            d.oDate.setHours(d.oWidget.oHourInput.getValue().isEmpty() ? 0 : d.oWidget.oHourInput.getValue().get());
            d.oDate.setMinutes(d.oWidget.oMinuteInput.getValue().isEmpty() ? 0 : d.oWidget.oMinuteInput.getValue().get());
            d.oDate.setSeconds(d.oWidget.oSecondInput.getValue().isEmpty() ? 0 : d.oWidget.oSecondInput.getValue().get())
        }
        d.oWidget.setValue(d.oWidget.createValue(d.oDate))
    };
    this.fMouseHandler = function (l) {
        if (Common.Browser.isOpera()) {
            l.target.style.display = "none";
            l.target.style.display = "table-cell"
        } else {
            var l = Common.Event.normalize(l);
            Common.Class[l.type == "mouseover" ? "add" : "remove"](l.target, d.__self.CLASS_NAME_HOVERED)
        }
    }
}, setDate:function (a) {
    this.oDate = a;
    if (this.isShowed()) {
        this.render()
    }
}, isShowed:function () {
    return this.bShowed
}, show:function () {
    if (this.isShowed()) {
        return
    }
    this.render();
    this.oWidget.addClass(this.__self.CLASS_NAME_PICKER_ACTIVE);
    Common.Class.remove(this.oElement.parentNode, this.__self.CLASS_NAME_HIDDEN);
    this.bShowed = true
}, hide:function () {
    if (!this.isShowed()) {
        return
    }
    Common.Class.add(this.oElement.parentNode, this.__self.CLASS_NAME_HIDDEN);
    this.oWidget.removeClass(this.__self.CLASS_NAME_PICKER_ACTIVE);
    this.bShowed = false
}, render:function () {
    this.oYearTitleElement.innerHTML = this.oDate.getFullYear();
    this.oMonthTitleElement.innerHTML = ZForms.Resources.getMonthsByType("normal")[this.oDate.getMonth()];
    var c = new Date(this.oDate.getFullYear(), this.oDate.getMonth(), 1), j = new Date(this.oDate.getFullYear(), this.oDate.getMonth(), -0.5).getDate(), m = (c.getDay() == 0 ? 7 : c.getDay()) - 1, l = new Date(this.oDate.getFullYear(), this.oDate.getMonth() + 1, -0.5), a = 7 - (l.getDay() == 0 ? 7 : l.getDay()), k = new Common.Utils.StringBuffer("<table>");
    for (var f = 1; f <= m; f++) {
        if (f % 7 == 1) {
            k.append(f > 1 ? "</tr>" : "").append("<tr>")
        }
        k.append('<td class="').append(this.__self.CLASS_NAME_ADD).append('"').append(f % 7 == 6 || f % 7 == 0 ? " " + this.__self.CLASS_NAME_WEEKEND : "").append('">').append(j - m + f).append("</td>")
    }
    for (var f = m + 1, g = l.getDate(), e = 1, d; e <= g; f++) {
        if (f % 7 == 1) {
            k.append("</tr><tr>")
        }
        d = "";
        if (e == this.oDateNow.getDate() && this.oDate.getMonth() == this.oDateNow.getMonth() && this.oDate.getYear() == this.oDateNow.getYear()) {
            d = this.__self.CLASS_NAME_NOW
        }
        if (f % 7 == 6 || f % 7 == 0) {
            d += (d.length > 0 ? " " : "") + this.__self.CLASS_NAME_WEEKEND
        }
        k.append("<td");
        if (d.length > 0) {
            k.append(' class="').append(d).append('"')
        }
        k.append(">").append(e++).append("</td>")
    }
    for (var f = m + g + 1, e = 1; e <= a; f++) {
        if (f % 7 == 1) {
            k.append("</tr><tr>")
        }
        k.append('<td class="').append(this.__self.CLASS_NAME_ADD).append(f % 7 == 6 || f % 7 == 0 ? " " + this.__self.CLASS_NAME_WEEKEND : "").append('">').append(e++).append("</td>")
    }
    k.append("</tr></table>");
    var b = document.createElement("div");
    b.innerHTML = k.get();
    b = b.getElementsByTagName("tbody")[0];
    Common.Event.remove(this.oElement, "click", this.fClickHandler);
    Common.Event.add(b, "click", this.fClickHandler);
    if (Common.Browser.isOpera() || (Common.Browser.isIE() && (!document.compatMode || document.compatMode == "BackCompat" || !window.XMLHttpRequest))) {
        var h = this.oElement.getElementsByTagName("td");
        for (var f = 0; f < h.length; f++) {
            Common.Event.remove(h[f], ["mouseover", "mouseout"], this.fMouseHandler)
        }
        h = b.getElementsByTagName("td");
        for (var f = 0; f < h.length; f++) {
            Common.Event.add(h[f], ["mouseover", "mouseout"], this.fMouseHandler)
        }
    }
    this.oElement.parentNode.replaceChild(b, this.oElement);
    this.oElement = b
}, setPrevMonth:function () {
    this.setDate(new Date(this.oDate.getFullYear(), this.oDate.getMonth(), -0.5))
}, setNextMonth:function () {
    this.setDate(new Date(this.oDate.getFullYear(), this.oDate.getMonth(), 33))
}, setPrevYear:function () {
    this.setDate(new Date(this.oDate.getFullYear() - 1, this.oDate.getMonth(), 1))
}, setNextYear:function () {
    this.setDate(new Date(this.oDate.getFullYear() + 1, this.oDate.getMonth(), 1))
}, enable:function () {
    this.oPickerButton.enable()
}, disable:function () {
    this.hide();
    this.oPickerButton.disable()
}, destruct:function () {
    this.oWidget = null;
    this.oElement = null;
    this.oYearTitleElement = null;
    this.oMonthTitleElement = null;
    this.oPickerButton.destruct()
}}, {CLASS_NAME_CALENDAR:"zf-calendar", CLASS_NAME_HIDDEN:ZForms.Widget.CLASS_NAME_HIDDEN, CLASS_NAME_ARROW_PREV:"zf-buttonprev", CLASS_NAME_ARROW_NEXT:"zf-buttonnext", CLASS_NAME_TITLE:"zf-title", CLASS_NAME_WEEKEND:"zf-weekend", CLASS_NAME_NOW:"zf-now", CLASS_NAME_ADD:"zf-add", CLASS_NAME_PICKER_ACTIVE:"zf-picker-active", CLASS_NAME_HOVERED:"zf-hovered"});
ZForms.Resources = {sLanguage:(document.documentElement.lang ? document.documentElement.getAttribute("lang") : "ru"), aMonths:{ru:{normal:["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"], genitive:["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]}, en:{normal:["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"], genitive:["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]}}, aDaysOfWeek:{ru:["пн", "вт", "ср", "чт", "пт", "сб", "вс"], en:["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}, aNumberSeparators:{ru:",", en:"."}, getNumberSeparator:function () {
    return this.aNumberSeparators[this.sLanguage]
}, getDaysOfWeek:function () {
    return this.aDaysOfWeek[this.sLanguage]
}, getMonthsByType:function (a) {
    return this.aMonths[this.sLanguage][a]
}};
ZForms.Builder = Abstract.inheritTo({__constructor:function (a) {
    this.oFormElement = a;
    this.oForm = null;
    this.aWidgets = [];
    this.aWidgetsById = [];
    this.aSheetContainers = [];
    this.aRepeatContainers = [];
    this.oLastRepeatRoot = null;
    this.aDependencies = [];
    var b = this;
    Common.Event.add(window, ZForms.Widget[Common.Browser.isIE() ? "DOM_EVENT_TYPE_BEFOREUNLOAD" : "DOM_EVENT_TYPE_UNLOAD"], function () {
        b.oFormElement = null
    })
}, $:function (a) {
    var b = document.getElementById(a);
    if (!b) {
        ZForms.throwException('Element with id "' + a + '" no exists')
    }
    return b
}, build:function () {
    this.oForm = this.createWidgetByElement(this.oFormElement);
    var e = Common.Dom.getElementsByClassName(this.oFormElement, this.__self.CLASS_NAME_WIDGET), d = e.length, a = [], c = 0;
    while (c < d) {
        a.push(this.createWidgetByElement(e[c++]))
    }
    var b, c = 0;
    while (b = a[c++]) {
        this.aWidgets[b.getName()] = b;
        this.aWidgetsById[b.getId()] = b
    }
    this.buildDependencies();
    if (this.oForm) {
        this.oForm.init()
    }
    delete this.oFormElement;
    delete this.aWidgets;
    delete this.aWidgetsById;
    delete this.aSheetContainers;
    delete this.aRepeatContainers;
    delete this.oLastRepeatRoot;
    delete this.aDependencies;
    return this.oForm
}, createWidgetByElement:function (c) {
    var b = this.extractParamsFromElement(c), f = b.sType, e = this.getParentWidget(b, f, c), d = ZForms[this.getCreateWidgetFunction(f)](c, this.getClassElement(b.sCId, f, c), this.processParams(b, e));
    if (b.oRepeatOptions && b.oRepeatOptions.sGroup) {
        this.oLastRepeatRoot = d
    }
    if (b.oRequired || b.oValid || b.oEnabled || b.oDependedOptions || b.oDependedClasses) {
        this.aDependencies.push({oWidget:d, oParams:b})
    }
    if (e) {
        if (b.oRepeatOptions && b.oRepeatOptions.sGroup && d.isTemplate()) {
            e.addTemplate(d)
        } else {
            if (f == "buttonprev" || f == "buttonnext") {
                e["add" + (f == "buttonprev" ? "Prev" : "Next") + "Button"](d)
            } else {
                if (f == "buttonadd" || f == "buttonremove" || f == "buttonup" || f == "buttondown") {
                    var a = f.match(/button(\w)(.+)/);
                    e.getMultiplier()["add" + a[1].toUpperCase() + a[2] + "Button"](d)
                } else {
                    e.addChild(d)
                }
            }
        }
    }
    return d
}, processParams:function (a, b) {
    if ((a.oRepeatOptions && a.oRepeatOptions.bTemplate) || (b && b.isTemplate())) {
        a.oOptions = Common.Object.extend({bTemplate:true}, a.oOptions)
    }
    if (!a.oOptions) {
        return
    }
    if (a.oOptions.sPickerId) {
        a.oOptions.oPickerOpenerElement = this.$(a.oOptions.sPickerId);
        delete a.oOptions.sPickerId
    }
    if (a.oOptions.sTabId) {
        a.oOptions.oElementLegend = this.$(a.oOptions.sTabId);
        delete a.oOptions.sTabId
    }
    if (a.oOptions.sListId) {
        a.oOptions.oOptionsElement = this.$(a.oOptions.sListId);
        delete a.oOptions.sListId
    }
    if (a.oOptions.sListShowId) {
        a.oOptions.oShowOptionsElement = this.$(a.oOptions.sListShowId);
        delete a.oOptions.sListShowId
    }
    return a.oOptions
}, getClassElement:function (b, c, a) {
    if (b) {
        return this.$(b)
    }
    if (c == "form" || c == "fieldset" || c == "sheet" || c == "slider" || c == "slidervertical" || c == "checkboxgroup" || c == "radiobuttongroup" || c == "submit" || c == "button" || c == "buttonprev" || c == "buttonnext" || c == "buttonadd" || c == "buttonremove" || c == "buttonup" || c == "buttondown") {
        return
    }
    if (c == "state" || c == "hidden") {
        return a.parentNode
    }
    return a.parentNode.parentNode
}, getParentWidget:function (a, c, b) {
    if (c == "sheet") {
        return this.getSheetContainer(a, b)
    }
    if (a.oRepeatOptions && a.oRepeatOptions.sGroup) {
        return this.getRepeatContainer(a, b)
    }
    if (c == "buttonprev" || c == "buttonnext") {
        return this.getSheet(b)
    }
    if (c == "buttonadd" || c == "buttonremove" || c == "buttonup" || c == "buttondown") {
        return this.getRepeatRoot(b)
    }
    if (c == "form") {
        return
    }
    if (a.sPId) {
        return this.oForm.getWidgetById(a.sPId)
    }
    while (b = b.parentNode) {
        console.log(b);
        if (b.tagName.toLowerCase() == "form" || Common.Class.match(b, this.__self.CLASS_NAME_WIDGET)) {
            return this.oForm.getWidgetById(this.__self.getId(b))
        }
    }
}, getRepeatContainer:function (a, b) {
    if (!this.aRepeatContainers[a.oRepeatOptions.sGroup]) {
        this.aRepeatContainers[a.oRepeatOptions.sGroup] = this.getParentWidget({}, null, b).addChild(ZForms.createMultiplicator(null, null, a.oRepeatOptions))
    }
    return this.aRepeatContainers[a.oRepeatOptions.sGroup]
}, getRepeatRoot:function () {
    return this.oLastRepeatRoot
}, getSheetContainer:function (a, b) {
    var c = a.sSheetGroup || this.__self.getId(b.parentNode);
    if (!this.aSheetContainers[c]) {
        a.sType = null;
        this.aSheetContainers[c] = this.getParentWidget(a, null, b).addChild(ZForms.createSheetContainer())
    }
    return this.aSheetContainers[c]
}, getSheet:function (a) {
    while (a = a.parentNode) {
        if (a.tagName.toLowerCase() == "form" || Common.Class.match(a, this.__self.CLASS_NAME_WIDGET)) {
            var b = this.oForm.getWidgetById(this.__self.getId(a));
            if (b instanceof ZForms.Widget.Container.Sheet) {
                return b
            }
        }
    }
}, extractParamsFromElement:function (a) {
    var b = a.onclick instanceof Function ? a.onclick() || {} : {};
    b.sType = b.sType || this.extractTypeFromElement(a);
    return b
}, extractTypeFromElement:function (d) {
    var c = d.tagName.toLowerCase(), b;
    if (c == "input") {
        b = d.type.toLowerCase();
        if (b == "radio" || b == "checkbox") {
            return"state"
        }
    }
    var a = d.className.match(this.__self.rTypePattern);
    if (a) {
        return a[1]
    }
    switch (c) {
        case"input":
            if (b == "search") {
                return"text"
            }
            return b;
            break;
        case"form":
        case"fieldset":
        case"select":
            return c;
            break;
        case"textarea":
            return"text";
            break
    }
    ZForms.throwException("can't extract widget type from element with id \"" + this.__self.getId(d) + '"')
}, getCreateWidgetFunction:function (a) {
    if (!this.__self.aTypesToCreateWidgetFunction[a]) {
        ZForms.throwException('Unsupported widget type "' + a + '"')
    }
    return"create" + this.__self.aTypesToCreateWidgetFunction[a]
}, getWidgetByName:function (a) {
    return this.aWidgets[a]
}, getWidgetById:function (a) {
    return this.aWidgetsById[a]
}, buildDependencies:function () {
    var a = this.aDependencies, d = this.aDependencies.length, c = 0, e, b;
    while (c < d) {
        e = a[c++];
        b = e.oParams;
        if (b.oRequired) {
            this.buildRequiredDependence(e.oWidget, b.oRequired)
        }
        if (b.oValid) {
            this.buildValidOrEnabledDependence(e.oWidget, b.oValid, ZForms.Dependence.TYPE_VALID)
        }
        if (b.oEnabled) {
            this.buildValidOrEnabledDependence(e.oWidget, b.oEnabled, ZForms.Dependence.TYPE_ENABLED)
        }
        if (b.oDependedOptions) {
            this.buildOptionsDependence(e.oWidget, b.oDependedOptions)
        }
        if (b.oDependedClasses) {
            this.buildClassesDependence(e.oWidget, b.oDependedClasses)
        }
    }
}, buildRequiredDependence:function (b, a) {
    var f = this.getLogic(a);
    a.aFrom = this.__self.prependToArray({iMin:a.iMin}, a.aFrom);
    var e = 0, c, d;
    while (c = a.aFrom[e++]) {
        d = this.getWidgetFrom(c, b);
        if (c.fFunction) {
            b.addDependence(ZForms.createFunctionDependence(d, {iType:ZForms.Dependence.TYPE_REQUIRE, fFunction:c.fFunction, iLogic:f, bInverse:c.bInverse}))
        } else {
            b.addDependence(ZForms.createRequiredDependence(d, {rPattern:c.rPattern, iLogic:f, iMin:c.iMin ? c.iMin : 1}))
        }
    }
}, buildValidOrEnabledDependence:function (a, c, g) {
    var f = this.getLogic(c), h;
    if (c.sType) {
        h = {sType:c.sType}
    } else {
        if (typeof(c.rPattern) != "undefined") {
            h = {rPattern:c.rPattern}
        } else {
            if (c.fFunction) {
                h = {fFunction:c.fFunction}
            } else {
                if (c.oCompare) {
                    h = {oCompare:c.oCompare}
                }
            }
        }
    }
    if (h) {
        Common.Object.extend(h, {sId:c.sId, sName:c.sName, bInverse:c.bInverse, sClassName:c.sClassName, bCheckForEmpty:c.bCheckForEmpty, bFocusOnEnable:c.bFocusOnEnable})
    }
    c.aFrom = this.__self.prependToArray(h, c.aFrom);
    var e = 0, b, d;
    while (b = c.aFrom[e++]) {
        d = this.getWidgetFrom(b, a);
        if (b.sType && b.sType == "email" && g == ZForms.Dependence.TYPE_VALID) {
            a.addDependence(ZForms.createValidEmailDependence(d, {iLogic:f, bInverse:b.bInverse, sClassName:b.sClassName, bCheckForEmpty:b.bCheckForEmpty}))
        } else {
            if (b.rPattern) {
                a.addDependence(ZForms["create" + (g == ZForms.Dependence.TYPE_VALID ? "Valid" : "Enabled") + "Dependence"](d, {rPattern:this.__self.toPattern(b.rPattern), iLogic:f, bInverse:b.bInverse, sClassName:b.sClassName, bCheckForEmpty:b.bCheckForEmpty, bFocusOnEnable:b.bFocusOnEnable}))
            } else {
                if (b.oCompare) {
                    if (b.oCompare.sCondition && !ZForms.Dependence.COMPARE_FUNCTIONS[b.oCompare.sCondition]) {
                        ZForms.throwException('unsupported type of compare condition: "' + b.oCompare.sCondition + '"')
                    }
                    a.addDependence(ZForms["create" + (g == ZForms.Dependence.TYPE_VALID ? "Valid" : "Enabled") + "CompareDependence"](d, {sCondition:b.oCompare.sCondition, mArgument:b.oCompare.sId ? this.getWidgetById(b.oCompare.sId) : (b.oCompare.sName ? this.getWidgetByName(b.oCompare.sName) : b.oCompare.mValue), iLogic:f, bInverse:b.bInverse, sClassName:b.sClassName, bCheckForEmpty:b.bCheckForEmpty, bFocusOnEnable:b.bFocusOnEnable}))
                } else {
                    if (b.fFunction) {
                        a.addDependence(ZForms.createFunctionDependence(d, {iType:g, fFunction:b.fFunction, iLogic:f, bInverse:b.bInverse}))
                    }
                }
            }
        }
    }
}, buildOptionsDependence:function (k, g) {
    var a = this.getLogic(g), c;
    if (g.aData) {
        c = {aData:g.aData}
    } else {
        if (g.fFunction) {
            c = {fFunction:g.fFunction}
        }
    }
    if (c) {
        Common.Object.extend(c, {sId:g.sId, sName:g.sName})
    }
    g.aFrom = this.__self.prependToArray(c, g.aFrom);
    var d = 0, b, e, h, f;
    while (e = g.aFrom[d++]) {
        h = this.getWidgetFrom(e, k);
        if (e.aData) {
            f = [];
            b = 0;
            while (b < e.aData.length) {
                f.push({rSource:this.__self.toPattern(e.aData[b][0]), rDestination:this.__self.toPattern(e.aData[b++][1])})
            }
            k.addDependence(ZForms.createOptionsDependence(h, {aPatterns:f, iLogic:a}))
        } else {
            if (e.fFunction) {
                k.addDependence(ZForms.createFunctionDependence(h, {iType:ZForms.Dependence.TYPE_OPTIONS, fFunction:e.fFunction, iLogic:a, bInverse:e.bInverse}))
            }
        }
    }
}, buildClassesDependence:function (k, a) {
    var b = this.getLogic(a), d;
    if (a.fFunction) {
        d = {fFunction:a.fFunction}
    } else {
        if (a.aData) {
            d = {aData:a.aData}
        }
    }
    if (d) {
        Common.Object.extend(d, {sId:a.sId, sName:a.sName})
    }
    a.aFrom = this.__self.prependToArray(d, a.aFrom);
    var e = 0, c, f, h, g;
    while (f = a.aFrom[e++]) {
        h = this.getWidgetFrom(f, k);
        if (f.aData) {
            g = [];
            c = 0;
            while (c < f.aData.length) {
                g.push({rPattern:this.__self.toPattern(f.aData[c][0]), sClassName:f.aData[c][1], bInverse:f.aData[c++][2]})
            }
            k.addDependence(ZForms.createClassDependence(h, {aPatternToClasses:g, iLogic:b}))
        } else {
            if (f.fFunction) {
                k.addDependence(ZForms.createFunctionDependence(h, {iType:ZForms.Dependence.TYPE_CLASS, fFunction:f.fFunction, iLogic:b, bInverse:f.bInverse}))
            }
        }
    }
}, getLogic:function (a) {
    return a.sLogic == "or" ? ZForms.Dependence.LOGIC_OR : ZForms.Dependence.LOGIC_AND
}, getWidgetFrom:function (a, c) {
    var b = a.sId ? this.getWidgetById(a.sId) : (a.sName ? this.getWidgetByName(a.sName) : c);
    if (!b) {
        this.throwDependenceException(a.sId || a.sName)
    }
    return b
}, throwDependenceException:function (a) {
    ZForms.throwException('Widget with name/id "' + a + '" no exists')
}}, {prependToArray:function (a, b) {
    if (typeof(a) == "undefined") {
        return b
    }
    if (!(a instanceof Array)) {
        a = [a]
    }
    if (!(b instanceof Array)) {
        b = []
    }
    return a.concat(b)
}, toPattern:function (a) {
    return a instanceof RegExp ? a : new RegExp("^" + a + "$")
}, getId:function (a) {
    return Common.Dom.getAttribute(a, "id") || Common.Dom.getUniqueId(a)
}, aTypesToCreateWidgetFunction:{form:"Form", text:"TextInput", password:"TextInput", file:"TextInput", hidden:"TextInput", number:"NumberInput", select:"SelectInput", combo:"ComboInput", date:"DateInput", submit:"SubmitButton", fieldset:"Container", checkboxgroup:"CheckBoxGroup", radiobuttongroup:"RadioButtonGroup", state:"StateInput", sheet:"Sheet", button:"Button", buttonprev:"Button", buttonnext:"Button", buttonadd:"Button", buttonremove:"Button", buttonup:"Button", buttondown:"Button", slider:"Slider", slidervertical:"SliderVertical"}, rTypePattern:/zf-(form|text|number|select|combo|date|submit|fieldset|checkboxgroup|radiobuttongroup|state|sheet|slider|slidervertical|buttonprev|buttonnext|buttonadd|buttonremove|buttonup|buttondown|button)(\s+|$)/, CLASS_NAME_WIDGET:"zf"});
Common.Event.add(document, Common.Event.TYPE_DOM_CONTENT_LOADED, function () {
    var c = Common.Dom.getElementsByClassName(document, ZForms.Builder.CLASS_NAME_WIDGET, "form"), b, a = 0;
    while (b = c[a++]) {
        if (!Common.Class.match(b, ZForms.Widget.Container.Form.CLASS_NAME_INITED)) {
            ZForms.buildForm(b)
        }
    }
    setTimeout(function () {
        ZForms.notifyObservers(ZForms.EVENT_TYPE_ON_INIT, ZForms);
        ZForms.bInited = true
    }, 1)
});