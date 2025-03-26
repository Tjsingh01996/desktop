package validators

import (
	"errors"
	"regexp"
)

type Validation struct {
	Message    string
	onValidate func(string) error
}

func (v *Validation) Validate(value string) error {
	return v.onValidate(value)
}

func Required(message string) *Validation {
	validation := &Validation{}
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

// NewMinLengthValidation checks if input length is at least `min`
func MinLength(min int, message string) *Validation {
	defaultMessage := "Input is too short"
	if message != "" {
		defaultMessage = message
	}

	return &Validation{
		onValidate: func(value string) error {
			if len(value) < min {
				return errors.New(defaultMessage)
			}
			return nil
		},
	}
}

// NewMaxLengthValidation checks if input length exceeds `max`
func MaxLength(max int, message string) *Validation {
	defaultMessage := "Input is too long"
	if message != "" {
		defaultMessage = message
	}

	return &Validation{
		onValidate: func(value string) error {
			if len(value) > max {
				return errors.New(defaultMessage)
			}
			return nil
		},
	}
}

func Email(message string) *Validation {
	defaultMessage := "Invalid email format"
	if message != "" {
		defaultMessage = message
	}

	return &Validation{
		onValidate: func(value string) error {
			emailRegex := `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
			matched, _ := regexp.MatchString(emailRegex, value)
			if !matched {
				return errors.New(defaultMessage)
			}
			return nil
		},
	}
}

func Password(minLength int, message string) *Validation {
	defaultMessage := "Password does not meet security requirements"
	if message != "" {
		defaultMessage = message
	}

	return &Validation{
		onValidate: func(value string) error {
			if len(value) < minLength {
				return errors.New(defaultMessage + " (too short)")
			}

			// At least one lowercase letter
			if matched, _ := regexp.MatchString(`[a-z]`, value); !matched {
				return errors.New(defaultMessage + " (missing lowercase letter)")
			}

			// At least one uppercase letter
			if matched, _ := regexp.MatchString(`[A-Z]`, value); !matched {
				return errors.New(defaultMessage + " (missing uppercase letter)")
			}

			// At least one digit
			if matched, _ := regexp.MatchString(`\d`, value); !matched {
				return errors.New(defaultMessage + " (missing number)")
			}

			// At least one special character
			if matched, _ := regexp.MatchString(`[!@#$%^&*(),.?":{}|<>]`, value); !matched {
				return errors.New(defaultMessage + " (missing special character)")
			}

			return nil
		},
	}
}
