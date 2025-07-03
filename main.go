package main

import (
	"context"
	"database/sql"
	"image/color"
	"log"

	_ "net/http/pprof" // Register pprof handlers

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/theme"
	"fyne.io/fyne/v2/widget"
	layouts "github.com/Tjsingh01996/desktop/Layouts"
	"github.com/Tjsingh01996/desktop/Pages"
	"github.com/Tjsingh01996/desktop/components"
	database "github.com/Tjsingh01996/desktop/db"
)

var db *sql.DB //
func main2() {
	a := app.New()
	a.Settings().SetTheme(newAppTheme(1))
	ctx := context.WithValue(context.Background(), "app", a)
	w := a.NewWindow("Hello")
	ctx = context.WithValue(ctx, "currentW", w)
	w.SetContent(makeGui(ctx))
	defer a.Quit()
	w.ShowAndRun()
}
func main() {
	log.SetFlags(log.LUTC | log.Ldate | log.Ltime | log.Lshortfile)
	// go func() {
	// 	log.Println("Starting pprof server on :6060")
	// 	if err := http.ListenAndServe("localhost:6060", nil); err != nil {
	// 		log.Fatal(err)
	// 	}
	// }()
	ctx, stop := context.WithCancel(context.Background())
	defer stop()
	myApp := app.New()
	database.GetDbConnection()

	myWindow := myApp.NewWindow("TabContainer Widget")
	ctx = context.WithValue(ctx, "currentW", myWindow)
	myApp.Settings().SetTheme(newAppTheme(theme.VariantLight))
	// chatPage := Pages.ChatBox(ctx)
	loginPage := Pages.LoginPage(ctx)
	myWindow.SetContent(loginPage)
	myWindow.Resize(fyne.NewSize(400, 300))
	myWindow.ShowAndRun()
}

func makeGui(ctx context.Context) fyne.CanvasObject {
	hello := widget.NewLabel("Hello Fyne what are you doing!")
	return Layout(ctx, hello)
}

func Layout(ctx context.Context, content fyne.CanvasObject) fyne.CanvasObject {
	gradient := components.CreateShadow()
	top := container.NewVBox(
		canvas.NewText("Hello Fyne!", color.Black),
		gradient, // Shadow under the text
	)
	sidebar := sideBar(ctx)
	layout := layouts.NewAppLayout(top, sidebar, nil, content)
	objs := []fyne.CanvasObject{top, sidebar, nil, content}
	return container.New(layout, objs...)
}
