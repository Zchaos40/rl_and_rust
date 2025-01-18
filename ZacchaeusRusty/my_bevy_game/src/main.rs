
use bevy::prelude::*;
// use bevy::sprite::Material2dPlugin;
use bevy::sprite::ColorMaterial;
use bevy::sprite::MaterialMesh2dBundle;
use bevy::color::palettes::basic::PURPLE;
use bevy::color::palettes::basic::BLUE;
use bevy::color::palettes::basic::YELLOW;
// use bevy::color::PURPLE;
use bevy::input::keyboard::KeyCode;
// use bevy::keyboard::KeyCode;
use rand::Rng;

const purple_purple:f32= 0.15;
const purple_blue:f32= 0.0;
const purple_yellow:f32= -0.2;
const blue_purple:f32= 0.0;
const blue_blue:f32= -0.1;
const blue_yellow:f32= -0.34;
const yellow_purple:f32 = 0.34;
const yellow_blue:f32= -0.17;
const yellow_yellow:f32= -0.32;



fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .insert_state(MyPausedState::Running)
        .add_systems(Startup, setup)
        .add_systems(Update, pauser)
        .add_systems(Update, rule1.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, rule2.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, rule3.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, rule4.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, rule5.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, rule6.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, rule7.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, rule8.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, rule9.run_if(in_state(MyPausedState::Running)))
        .add_systems(Update, cursorstuff)
        .run();
}

#[derive(Component)]
struct Purple_a;

#[derive(Component)]
struct Blue_a;

#[derive(Component)]
struct Yellow_a;

fn cursorstuff(mut events: EventReader<CursorMoved>) { 
    for e: &CursorMoved in events {
        println!("cursor is at: {:?}", e)
    }
}

fn setup(
    mut commands: Commands,
    mut materials: ResMut<Assets<ColorMaterial>>,
    mut meshes: ResMut<Assets<Mesh>>,
) {
    commands.spawn((
        Camera2dBundle {
            projection: OrthographicProjection {
                // don't forget to set `near` and `far`
                near: -500.0,
                far: 500.0,
                // ... any other settings you want to change ...
                ..default()
            },
            ..default()
        }
    ));
    // Define the number of particles to spawn
    let num_particles = 300;

    // Create a random number generator
    let mut rng = rand::thread_rng();

    //yellowgreen, bluered, purpleyello

    for _ in 0..num_particles {
        // Generate random positions within a certain range
        let x = rng.gen_range(-500.0..500.0);
        let y = rng.gen_range(-500.0..500.0);

        // Spawn a Purple_a particle
        commands.spawn((
            MaterialMesh2dBundle {
                mesh: meshes.add(Rectangle::default()).into(),
                transform: Transform::from_xyz(x, y, 0.0).with_scale(Vec3::splat(10.0)),
                material: materials.add(Color::from(PURPLE)),
                ..default()
            },
            Purple_a,
        ));

        // Spawn a Blue_a particle
        commands.spawn((
            MaterialMesh2dBundle {
                mesh: meshes.add(Rectangle::default()).into(),
                transform: Transform::from_xyz(x, y, 0.0).with_scale(Vec3::splat(10.0)),
                material: materials.add(Color::from(BLUE)),
                ..default()
            },
            Blue_a,
        ));
        commands.spawn((
            MaterialMesh2dBundle {
                mesh: meshes.add(Rectangle::default()).into(),
                transform: Transform::from_xyz(x, y, 0.0).with_scale(Vec3::splat(10.0)),
                material: materials.add(Color::from(YELLOW)),
                ..default()
            },
            Yellow_a,
        ));
        // commands.spawn((
        //     MaterialMesh2dBundle {
        //         mesh: meshes.add(Rectangle::default()).into(),
        //         transform: Transform::default().with_scale(Vec3::splat(10.)),
        //         material: materials.add(Color::from(BLUE)),
        //         ..default()
        //     },
        //     Direction::Up,
        //     Blue_a{},
        // ));
    }
}

// fn setup(    
//     mut commands: Commands,
//     mut materials: ResMut<Assets<ColorMaterial>>,
//     mut meshes: ResMut<Assets<Mesh>>,) {
//     commands.spawn(Camera2dBundle::default());
//     commands.spawn((
//         MaterialMesh2dBundle {
//             mesh: meshes.add(Rectangle::default()).into(),
//             // transform: Transform::from_xyz(100., 0., 0.),
//             transform: Transform::default().with_scale(Vec3::splat(10.)),
//             material: materials.add(Color::from(PURPLE)),
//             ..default()
//         },
//         Direction::Up,
//         Purple_a{},
//     ));
//     commands.spawn((
//         MaterialMesh2dBundle {
//             mesh: meshes.add(Rectangle::default()).into(),
//             // transform: Transform::from_xyz(100., 0., 0.),
//             transform: Transform::default().with_scale(Vec3::splat(10.)),
//             material: materials.add(Color::from(BLUE)),
//             // Blue_a
//             ..default()
//         },
//         Direction::Up,
//         Blue_a{},
//     ));
    
// }

#[derive(States, Default, Debug, Clone, PartialEq, Eq, Hash)]
enum MyPausedState {
    #[default]
    Paused,
    Running,
}

// if keys.just_pressed(KeyCode::Space)
fn pauser(
    keys: Res<ButtonInput<KeyCode>>,
    state: Res<State<MyPausedState>>,
    mut next_state: ResMut<NextState<MyPausedState>>,
) {
    // if keys.just_pressed(Keycode::Space) {
        if keys.pressed(KeyCode::Space) {
        match state.get() {
            MyPausedState::Paused => next_state.set(MyPausedState::Running),
            MyPausedState::Running => next_state.set(MyPausedState::Paused),
    }}
}

fn rule1(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Blue_a>>,
        Query<&Transform, With<Purple_a>>,
    )>
) {
    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = blue_purple * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}

fn rule2(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Purple_a>>,
        Query<&Transform, With<Blue_a>>,
    )>
) {
    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = purple_blue * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}

 
fn rule3(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Purple_a>>,
        Query<&Transform, With<Purple_a>>,
    )>
) {
    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = purple_purple * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}

fn rule4(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Blue_a>>,
        Query<&Transform, With<Blue_a>>,
    )>
) {
    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = blue_blue * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}





fn rule5(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Yellow_a>>,
        Query<&Transform, With<Yellow_a>>,
    )>
) {

    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = yellow_yellow * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    
    
    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}

fn rule6(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Yellow_a>>,
        Query<&Transform, With<Blue_a>>,
    )>
) {
    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = yellow_blue * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    
    
    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}

fn rule7(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Blue_a>>,
        Query<&Transform, With<Yellow_a>>,
    )>
) {
    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = blue_yellow * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    
    
    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}

fn rule8(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Purple_a>>,
        Query<&Transform, With<Yellow_a>>,
    )>
) {
    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = purple_yellow * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    
    
    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}

fn rule9(
    mut param_set: ParamSet<(
        Query<&mut Transform, With<Yellow_a>>,
        Query<&Transform, With<Purple_a>>,
    )>
) {
    // Collect all Purple_a transforms in a separate vector to avoid borrowing p0 twice
    let purple_transforms: Vec<_> = param_set.p0().iter().map(|t| t.translation).collect();

    // Create a vector to store the forces for each Purple_a entity
    let mut forces: Vec<(f32, f32)> = vec![];

    // First loop: calculate the forces for each Purple_a based on the Blue_a entities
    for transform in &purple_transforms {
        let mut fx = 0.0;
        let mut fy = 0.0;

        // Second loop: iterate over Blue_a entities to calculate the force
        for transform2 in param_set.p1().iter() {
            let dx = transform.x - transform2.translation.x;
            let dy = transform.y - transform2.translation.y;
            let d = (dx * dx + dy * dy).sqrt();

            if d > 0.0 && d < 120.0 {
                let F = yellow_purple * 1.0 / d;
                fx += F * dx;
                fy += F * dy;
            }
        }

        // Store the calculated forces
        forces.push((fx, fy));
    }

    
    
    // Now, apply the calculated forces to the Purple_a entities (mutably)
    for (mut transform, (fx, fy)) in param_set.p0().iter_mut().zip(forces.iter()) {
        transform.translation.x += fx;
        transform.translation.y += fy;

        // Boundary checks
        if transform.translation.x < -500.0 {
            transform.translation.x +=1000.0;
        }
        if transform.translation.x > 500.0 {
            transform.translation.x-=1000.0;
        }
        if transform.translation.y < -300.0 {
            transform.translation.y+= 600.0;
        }
        if transform.translation.y > 300.0 {
            transform.translation.y -=600.0;
        }
    }
}

// fn rule(mut particles1:Query<&mut Transform, With<Purple_a>>, particles2:Query<&Transform, With<Blue_a>>) {
//     for mut transform in &mut particles1{
//         let mut fx=0.0;
//         let mut fy=0.0;
//         for mut transform2 in &mut particles2{
            
//             // let mut a = particles1;
//             // let mut b = particles2; 
//             let mut dx = transform.translation.x-transform2.translation.x;
//             let mut dy = transform.translation.y-transform2.translation.y;
//             let mut thangity = dx*dx+dx*dy;
//             let mut d = thangity.sqrt();
//             if d>0.0{
//                 if d<80.0{
//                     let mut F = 1.0*1.0/d;
//                     let mut fx = fx+(F*dx);
//                     let mut fy = fy+(F*dy);
//             }}}}
//         //}
//         //make particle velocity go up by numbers(particle_velocityx=particle_velocityx+fx)*0.5 
//         transform.translation.x = (transform.translation.x +fx);
//         transform.translation.y = (transform.translation.y +fy);
//         //make particle's x and y change by fx and fy here. (particle_x+=particle_velocityx)
//         //also, to reverse velocity when hit wall:
//         // if particle_x<=0{particle_velocityx=particle_velocityx*-1}
//         // if particle_x>=500{particle_velocityx=particle_velocityx*-1}
//     //}
// }

// fn sprite_movement(
//     time: Res<Time>,
//     mut sprite_position: Query<(&mut Direction, &mut Transform, &mut Colored)>,
// ) {
//     for (mut logo, mut transform, colored) in &mut sprite_position {
//         match *colored {
//             Colored::Bluea=>{
//                 match *logo {
//                 Direction::Up => transform.translation.y += 150. * time.delta_seconds(),
//                 Direction::Down => transform.translation.y -= 150. * time.delta_seconds()
//             }}
//             Colored::Purplea => { match *logo {
//                 Direction::Up => transform.translation.y -= 150. * time.delta_seconds(),
//                 Direction::Down => transform.translation.y += 150. * time.delta_seconds() }}
//             Colored::Reda => { }
//             Colored::Greena => {  }
//             Colored::Orangea => {  }
//             Colored::Yellowa => { }};

//         if transform.translation.y > 200. {
//             *logo = Direction::Down;
//         } else if transform.translation.y < -200. {
//             *logo = Direction::Up
//         }
//     }
// }
// ! Shows how to render a polygonal [`Mesh`], generated from a [`Rectangle`] primitive, in a 2D scene.

// use bevy::{color::palettes::basic::PURPLE, prelude::*, sprite::MaterialMesh2dBundle};

// fn main() {
//     App::new()
//         .add_plugins(DefaultPlugins)
//         .add_systems(Startup, setup)
//         .run();
// }

// fn setup(
//     mut commands: Commands,
//     mut meshes: ResMut<Assets<Mesh>>,
//     mut materials: ResMut<Assets<ColorMaterial>>,
// ) {
//     commands.spawn(Camera2dBundle::default());
//     commands.spawn(MaterialMesh2dBundle {
//         mesh: meshes.add(Rectangle::default()).into(),
//         transform: Transform::default().with_scale(Vec3::splat(128.)),
//         material: materials.add(Color::from(PURPLE)),
//         ..default()
//     });
// }