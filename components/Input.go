package components

import (
	"errors"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

type InputType int

// Enum values using iota
const (
	Text InputType = iota
	Password
)

type AppInput struct {
	widget.Entry
	size            fyne.Size
	variant         InputType
	validations     []Validation
	invalid         bool
	validationError error
}

func (i *AppInput) Input() *fyne.Container {
	switch i.variant {
	case Password:
		i.Password = true
	}
	if i.PlaceHolder != "" {
		i.SetPlaceHolder(i.PlaceHolder)
	}
	i.SetValidationError(errors.New("widget.FormItem initial state error"))
	i.Resize(fyne.NewSize(300, 400))
	i.Validator = i.validate
	i.SetOnValidationChanged(i.onUpdateValidation)

	return container.NewVBox(
		i,
	)
}

func (i *AppInput) validate(s string) error {
	if i.validations == nil {
		return nil
	}
	var err error
	for k := 0; k < len(i.validations); k++ {
		err = i.validations[k].Validate(s)
		if err != nil {
			// form use that this key to check validation
			i.validationError = err
			return err
		}
	}
	return nil
}

func (i *AppInput) SetValidations(validations ...Validation) {
	i.Validator = i.validate
	i.validations = validations
}

func (i *AppInput) MinSize() fyne.Size {
	if i.size.Width != 0 && i.size.Width != 0 {
		return i.size
	}
	return fyne.NewSize(300, 50)
}

func (i *AppInput) setSize(size fyne.Size) {
	i.size = size
}

func (i *AppInput) SetMinSize(size fyne.Size) {
	i.size = size
}

func (i *AppInput) onUpdateValidation(err error) {

}

func NewPasswordInput() *AppInput {
	entry := NewInput()
	entry.Password = true
	return entry
}

func NewInput() *AppInput {
	input := &AppInput{}
	input.ExtendBaseWidget(input) // Important: This initializes the custom widget
	return input
}

type Validation interface {
	Validate(input string) error
}

type AppValidation struct {
	Message    string
	onValidate func(string) error
}

func (v *AppValidation) Validate(value string) error {
	return v.onValidate(value)
}

func NewRequiredValidation(message string) *AppValidation {
	validation := &AppValidation{}
	defaultMessage := "Required Field"
	if message != "" {
		defaultMessage = message
	}
	validation.onValidate = func(e string) error {
		if len(e) == 0 {
			return errors.New(defaultMessage)
		}
		return nil
	}
	return validation
}

type CustomFormItem struct {
	widget.FormItem
}
