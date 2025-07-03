package Pages

import (
	"context"
	"image/color"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/layout"
	"fyne.io/fyne/v2/widget"
	"github.com/Tjsingh01996/desktop/components"
	"github.com/Tjsingh01996/desktop/pkg/validators"
	"github.com/Tjsingh01996/desktop/service"
)

func LoginPage(ctx context.Context) *fyne.Container {
	return loginForm(ctx)
}

func loginForm(ctx context.Context) *fyne.Container {
	authService := service.GetAuthService()
	currentW := ctx.Value("currentW").(fyne.Window)
	formLabel := canvas.NewText("Login", color.Black)
	formLabel.TextStyle.Bold = true
	formLabel.TextSize = 24

	userNameInput := components.NewInput()
	userNameInput.SetMinSize(fyne.NewSize(400, 50))
	requiredValidations := validators.Required("")
	minLengthValidation := validators.MinLength(8, "")
	userNameInput.SetValidations(requiredValidations, minLengthValidation)
	userNameInput.SetPlaceHolder("User Name")

	passwordProps := components.NewPasswordInput()
	// passwordValidator := validators.Password(8, "")
	// passwordProps.SetValidations(passwordValidator)
	passwordProps.SetPlaceHolder("Password")

	form := widget.NewForm(
		widget.NewFormItem("Name", userNameInput),
		widget.NewFormItem("Email", passwordProps),
	)
	form.OnSubmit = func() {
		user, err := authService.Login(ctx, userNameInput.Text, passwordProps.Text)
		if err != nil {
			components.ShowError("Login Error", err, currentW)
			return
		}
		if user["id"] == nil {
			return
		}
		ctx = context.WithValue(ctx, "currentUser", user)
		chat := ChatBox(ctx)
		currentW.SetContent(chat)
	}
	form.SetOnValidationChanged(func(err error) {
	})
	label := container.New(layout.NewCenterLayout(), formLabel)
	fixedSpace := container.New(layout.NewGridWrapLayout(fyne.NewSize(200, 60)))
	layout.NewCustomPaddedLayout(20, 20, 20, 20)
	formLayout := container.New(layout.NewVBoxLayout(),
		label,
		fixedSpace,
		form,
	)
	formLayout = container.New(layout.NewCustomPaddedLayout(30, 30, 30, 30), formLayout)
	card := widget.NewCard("", "", formLayout)
	outerContainer := container.New(layout.NewCenterLayout(), card)

	return outerContainer

}
