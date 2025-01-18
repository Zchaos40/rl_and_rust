use bevy::prelude::*;
// use bevy::prelude::App;
// use bevy::prelude::Update;
// use bevy::prelude::Commands;
// use bevy::prelude::Startup;
// use bevy::prelude::Component;
// pub struct HelloPlugin;

// impl Plugin for HelloPlugin {
//     fn build(&self, app: &mut App) {
//         app.insert_resource(GreetTimer(Timer::from_seconds(2.0, TimerMode::Repeating)));
//         app.add_systems(Startup, add_people);
//         app.add_systems(Update, (update_people, greet_people).chain());
//     }
// }

#[derive(Component)]
struct X();

// #[derive(Component)]
// struct Person;

#[derive(Component)]
struct Name(String);

#[derive(Component)]
struct Descriptor(String);

// #[derive(Resource)]
// struct GreetTimer(Timer);

// fn number2() {
//     println!("{}" )
// }

fn querytester(query: Query<&X>){

    for &name in query:
        println!("{}", name.0)

}

fn main() {

    commands.spawn(X, Descriptor("1").to_string());
    commands.spawn(Descriptor("2").to_string());
    commands.spawn(X, Descriptor("3").to_string());
    commands.spawn(Descriptor("4").to_string());
    commands.spawn(Descriptor("5").to_string());
    commands.spawn(X, Descriptor("6").to_string());

    App::new()
        .add_plugins(DefaultPlugins)
        // .add_plugins(HelloPlugin)
        .add_plugins(querytester(bevy::prelude::Query<'_, '_, &X>))
        .run();
}

// fn update_people(mut query: Query<&mut Name, With<Person>>) {
//     for mut name in &mut query {
//         if name.0 == "Elaina Proctor" {
//             name.0 = "Elaina Hume".to_string();
//             break; // We don't need to change any other names.
//         }
//     }
// }

// fn greet_people(time: Res<Time>, mut timer: ResMut<GreetTimer>, query: Query<&Name, With<Person>>) {
//     // update our timer with the time elapsed since the last update
//     // if that caused the timer to finish, we say hello to everyone
//     if timer.0.tick(time.delta()).just_finished() {
//         for name in &query {
//             println!("hello {}!", name.0);
//         }
//     }
// }

// fn add_people(mut commands: Commands) {
//     commands.spawn((Person, Name("Elaina Proctor".to_string())));
//     commands.spawn((Person, Name("Renzo Hume".to_string())));
//     commands.spawn((Person, Name("Zayna Nieves".to_string())));
// }

// fn hello_world() {
//     println!("hello world!");
// }
