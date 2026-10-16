```{=latex}
\begin{titlepage}
\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
  % Cover laid out absolutely; coordinates are pt from the top-left of the page, matching
  % the reference cover. Manual title centred at y≈262; logo mark from y≈108, 112pt tall.
  % The brand logo replaces the earlier LITEARM SE wordmark.
  \node[anchor=north,inner sep=0pt] at ($(current page.north west)+(298.75pt,-108.9pt)$)
      {\includegraphics[width=100pt,height=112pt,keepaspectratio]{LITEARM_SE_images/cover_litearm_logo.png}};
  \node[anchor=center] at ($(current page.north west)+(298.75pt,-262.4pt)$)
      {{\fontsize{28}{34}\selectfont\sffamily\bfseries Product Manual}};
  \node[anchor=north,inner sep=0pt] at ($(current page.north west)+(298.75pt,-300.8pt)$)
      {\includegraphics[width=289.1pt,height=289.1pt,keepaspectratio]{LITEARM_SE_images/cover_litearm_se.png}};
  \node[anchor=center] at ($(current page.north west)+(298.75pt,-717.8pt)$)
      {{\fontsize{11}{14}\selectfont\bfseries NEXFORM ROBOTICS}};
  \node[anchor=center] at ($(current page.north west)+(298.75pt,-747.9pt)$)
      {{\fontsize{9}{13}\selectfont Version: V1.0.4\qquad Date: October 16, 2026}};
\end{tikzpicture}
\end{titlepage}
\pagenumbering{Roman}
\thispagestyle{frontmatter}
\section*{Revision History}
```

| Version | Date | Revision |
|---|---|---|
| V1.0.4 | 2026-10-16 | Removed the whole chapter on installing and using the arm; installation steps now point to the LITEARM-SE installation guide. Updated the FAQ |
| V1.0.3 | 2026-10-16 | Control moved to the on-board control board, with the host PC connected directly over USB. Updated the electrical interfaces and the wiring notes |
| V1.0.2 | 2026-09-03 | Added the installation notes and the electrical interface description |
| V1.0.1 | 2026-08-01 | First draft of the LITEARM SE product manual |

```{=latex}
\clearpage
\thispagestyle{frontmatter}
\tableofcontents
\clearpage
\pagenumbering{arabic}
\makeatletter\def\fps@figure{H}\makeatother
```


# Introduction

LITEARM SE is a 7-DoF collaborative robotic arm from NEXFORM ROBOTICS, built for research and teaching, AI robotics development, and lightweight industrial automation. It uses a modular joint architecture and has a working radius of about 650 mm. The arm is driven by a single **on-board control board**: the board runs the firmware and carries trajectory planning, forward and inverse kinematics, dynamics and the joint control law. Inside the arm the board talks to the joints over CAN — a board-level bus that you neither wire nor configure. Between the host PC and the board there is exactly **one USB cable**. Software on the PC side — the Python and C++ SDKs, ROS 2, the URDF, the PyBullet and MuJoCo simulations — only sends commands and reads state. It covers assembly, sorting, grasping, hand-guiding and algorithm validation.

## What is in the box

The standard kit contains the following. The sales configuration list is the final authority.

| No. | Item | Notes |
|:---:|---|---|
| 1 | Arm | LITEARM SE, 7 joints |
| 2 | Control board | On-board controller, ships with the arm |
| 3 | USB cable | Control board to host PC |
| 4 | Arm power lead | Power take-off for the arm |
| 5 | 600 W switching power supply kit | Optional |
| 6 | Desktop mounting kit | Optional |
| 7 | Column stand kit | Optional |
| 8 | Electric gripper | Optional |
| 9 | 3D camera | Optional |


## Units

This document and the SDK use the following units:

| Quantity | Unit | Notes |
|---|---|---|
| X / Y / Z | m | Position, in metres |
| R / P / Y | rad | Orientation, in radians |
| Joint angle | rad | Radians |
| vTCP | m/s | Tool linear velocity |
| aTCP | m/s² | Tool acceleration |
| vJoint | rad/s | Joint velocity |
| aJoint | rad/s² | Joint acceleration |
| Mass / payload | kg | Kilograms |
| Torque | N·m | Newton-metres |
| Voltage / power | VDC / W | Volts / watts |

> **Pose format.** A pose is **six numbers**: the first three are position `x, y, z` in metres, the last three are orientation `rx, ry, rz` in radians — rotations about the base frame's X, Y and Z axes, that is RPY angles. For example `(0.30, 0.0, 0.40, 3.1416, 0.0, 0.0)`. The Python SDK accepts either a list or a tuple; see the LITEARM SE software development manual.

## Safety

### Scope

This section states the safety principles you must follow when using the LITEARM SE arm and any system built around it. Read this manual before installing or using the arm, and treat every passage marked with a warning sign as mandatory. A moving arm can pinch, collide and fall. Take the risk of operating it seriously, and use the SDK or the control software only after training.

### Warning signs

The safety notices elsewhere in this manual use the signs below, shown in Figure 1. The markings on the delivered product are the authority.

- **DANGER**: a hazard that will cause death or serious injury, or severe equipment damage.
- **WARNING**: a hazard that can cause death or serious injury, or severe equipment damage, if it is not avoided.
- **HIGH TEMPERATURE**: hot parts, where contact can cause burns or damage equipment.
- **NOTICE**: a general caution, where failure to avoid the hazard can cause injury or equipment damage.

```{=latex}
\begin{figure}[H]
\centering
\makebox[\linewidth][c]{%
\begin{minipage}[b]{0.16\linewidth}\centering
\includegraphics[width=0.95\linewidth,keepaspectratio]{LITEARM_SE_images/safety/en/danger.png}
\end{minipage}\hspace{0.08\linewidth}%
\begin{minipage}[b]{0.16\linewidth}\centering
\includegraphics[width=0.95\linewidth,keepaspectratio]{LITEARM_SE_images/safety/en/warning.png}
\end{minipage}}\par\vspace{0.6em}%
\makebox[\linewidth][c]{%
\begin{minipage}[b]{0.16\linewidth}\centering
\includegraphics[width=0.95\linewidth,keepaspectratio]{LITEARM_SE_images/safety/en/high_temp.png}
\end{minipage}\hspace{0.08\linewidth}%
\begin{minipage}[b]{0.16\linewidth}\centering
\includegraphics[width=0.95\linewidth,keepaspectratio]{LITEARM_SE_images/safety/en/notice.png}
\end{minipage}}
\caption{Warning signs}
\end{figure}
```

### Safety notices

Understand and follow the following before starting the arm or the system around it for the first time.

#### Operating the arm

1. Install the arm, the control board and the electrical equipment exactly as this manual requires.
2. Have a qualified person inspect the arm and its safeguards before first use, and test every safety function: emergency stop, soft limits and the enable state.
3. Before each use, check that the equipment is complete and firmly mounted, and that it complies with the workplace safety regulations of your region.
4. Give the arm enough room to move. Keep people, obstacles and loose cables out of its working envelope.
5. Read the documentation before developing against the SDK or the host application, and make sure the inputs you send — target joint angles, speed, payload — are correct.
6. **After `disable()` or an unexpected power loss the joints stop producing torque, and the arm can fall under gravity.** Move the arm to a safe pose first, or hold it by hand in zero-gravity mode, so that nothing falls from height and injures someone or damages equipment.
7. If anything unexpected happens while the arm is moving, press the hardware emergency stop and cut the power before investigating.
8. Slew-rate limiting, joint soft limits, rejection of illegal values, the communication watchdog and the emergency stop fallback all live in the control board firmware and **do not depend on the host PC being connected**. The firmware only enforces hard limits, though: never let untrained people change parameters through the SDK — joint limits, PD gains, payload mass and centre of mass, gravity direction. Some of those changes require a fresh safety assessment.

#### People

1. Read the product manual, and know the safe and correct operating procedure and how to handle errors.
2. While the equipment is powered, treat the arm as moving even when it looks stopped — it may be waiting for a command.
3. Know the envelope of the arm and of the end effector — gripper, dexterous hand — and define a safe working area.
4. Inspect the arm regularly so that mounting bolts and the end tool cannot work loose.
5. When hand-guiding in zero-gravity mode, remember the arm's weight and its momentum, and do not let it suddenly lose support. Once you take your hands off, the arm should hold its pose; if it does not, stop.

### Responsibility

The arm can be integrated into a complete system, and this document does not cover the design, installation and operation of that complete system. How safe the finished system is depends on how it is integrated. You are responsible for assessing the design and installation risk of the complete system against the laws and safety standards of your country or region, and for putting the corresponding safeguards in place.

Using this arm means you have read, understood and accepted every term of this manual and of the safety information in it. You accept responsibility for your own actions and their consequences, and you will put the arm only to legitimate use. We accept no liability for injury, accidents or property damage caused by use outside these requirements or by events beyond our control. Your obligations include assessing the risk of the complete system, writing the operating procedure, establishing the safeguards, confirming that the system is designed and installed correctly, and not modifying the safeguards on your own.

### Risk assessment

A risk assessment has to cover every possible contact between people and the arm in normal use and in foreseeable misuse, for example:

- sharp end effectors or tool connectors;
- toxic or otherwise hazardous materials being handled;
- fingers caught in the base or in a joint;
- being struck by the arm;
- a poorly secured end tool, or a payload beyond range, falling;
- impact between the payload and a rigid surface.

Only your risk assessment can decide whether a hazard is an unacceptable risk, and it is what tells you which safeguards to add. The arm is not suitable for use by anyone without full legal capacity who is not under the supervision of a qualified person.

---

# Specifications

## General

| Parameter | Value |
|---|---|
| Product name | LITEARM SE 7-DoF collaborative robotic arm |
| Mounting | Upright / side / inverted |
| Degrees of freedom | 7 |
| Payload: rated / maximum | 3 kg / 5 kg |
| Arm weight | 5.6 kg |
| Repeatability | ±0.1 mm |
| Working radius | 650 mm |
| Supply voltage | DC 24 V |
| Rated power | 430 W |
| Speed scaling | 0.6 to 1.0 |
| Power supply | 600 W, with bleed |
| Control | On-board control board, ships with the arm |
| Communication | USB from host PC to control board; CAN from control board to joints, a board-level bus that you neither wire nor configure |
| Body material | Metal and high-strength engineering plastic composite |

## Control board

| Parameter | Value |
|---|---|
| Name | Control board, ships with the arm |
| Role | Trajectory planning, kinematics, dynamics and the control law, plus the safety fallbacks: emergency stop and soft limits |
| Firmware version | The factory version string looks like `Litearm1.5.0-7J` — `Litearm`, three version fields, then `-7J` for seven axes. The SDK requires `Litearm1.5.0` or later |
| Supply input | DC 24 V, XT60 connector |
| Host interface | USB, as a virtual serial port |
| Joint interface | Connects to the port under the arm |
| Parameter storage | On-board storage, with a per-unit dynamics calibration done at the factory |


## Joint parameters

To keep the arm safe, every joint angle has a software soft limit **baked into the control board firmware**, checked in real time while the arm moves. The SDK can read and configure them joint by joint, though changing one needs a safety assessment first:

```python
for jp in arm.params.all_joint_params():      # read back joint by joint
    print(jp.idx, jp.q_min, jp.q_max)         # or one axis: arm.params.get_joint_param(0)
arm.params.set_joint_limits(0, -2.8, 2.8)     # write joint by joint: narrows only
```

> `params.set_joint_limits()` **only narrows a limit.** Writing back the current value counts as a request to widen it and is rejected. A write persists only after `save_params()`, which writes Flash and cannot be undone. The table below is the factory nominal range; what the SDK reads back is what actually applies.

| Joint (URDF) | SDK index | Role | Range (rad) | Range (°) | Max speed (nominal) |
|---|---|---|---|---|---|
| Joint1 | q[0] | Base rotation | −2.809547 to 2.809547 | −161° to 161° | 180°/s |
| Joint2 | q[1] | Shoulder pitch | −1.727547 to 1.727547 | −99° to 99° | 180°/s |
| Joint3 | q[2] | Elbow pitch | −2.809547 to 2.809547 | −161° to 161° | 180°/s |
| Joint4 | q[3] | Wrist roll | −3.071547 to 0.017547 | −176° to +1° | 225°/s |
| Joint5 | q[4] | Wrist pitch | −2.809547 to 2.809547 | −161° to 161° | 225°/s |
| Joint6 | q[5] | Wrist yaw | −1.553547 to 1.553547 | −89° to 89° | 225°/s |
| Joint7 | q[6] | Tool rotation | −1.553547 to 1.553547 | −89° to 89° | 225°/s |

> **Notes**
> 1. Joint speed: the 1 rad/s default in the URDF is a simulation reference, not a statement of what the arm can do.
> 2. Joint4's range is asymmetric: −176° to +1°.
> 3. Maximum joint torque: the shoulder reaches about 97 N·m. For the other joints the authority is the per-joint firmware parameter `tau_max`, read back with `arm.params.get_joint_param(idx).value.tau_max`; the URDF `effort` values are Joint1 and 2 = 30, Joint3 and 4 = 9, Joint5 to 7 = 3.5 N·m.

## Figures

### Home pose and frames

- With the arm mounted the default way — on a tabletop, base horizontal — the base frame has its origin at the centre of the base mounting face, with Z pointing straight up, opposite the default gravity direction, and X and Y in the mounting plane following the right-hand rule. The tool frame, TCP, sits at the end flange. Figure 2 marks the base and tool frames. The URDF and the simulations (`base_link` and `ee_frame_link`) and the real arm are the authority on the actual orientation.

![Zero pose and frame annotations](LITEARM_SE_images/placeholders/ph_pm_coord.png)

- Gravity compensation carries the mounting orientation — upright, side or inverted. `set_gravity_vector(g)` sets the gravity direction and `set_gravity_scale(gs)` scales the gravity feed-forward joint by joint. Configure either one wrongly and gravity compensation is off.

### Joint rotation directions

Each joint turns about the axis its URDF defines, with the positive direction given by the **right-hand rule**. Figure 3 marks the direction of every joint. You can verify each one in the PyBullet or MuJoCo simulation, or under real-time control from the host application.

![Joint rotation direction annotations](LITEARM_SE_images/placeholders/ph_pm_rotdir.png)

---

# FAQ

## Q&A

**Q: Which control and motion modes does the arm have?**
A: LITEARM SE supports joint-space motion (`movej`), Cartesian lines, arcs and waypoint paths (`move_l`, `move_c`, `move_path`), Cartesian point-to-point (`move_p`), homing (`home`) and zero-gravity hand-guiding (`zero_g`); the development manual covers each one. Before any motion, make sure the arm is enabled and not in emergency stop.

**Q: What is the difference between joint space and Cartesian space?**
A: Joint space commands each joint angle directly. It is simple and rarely runs into a singularity, which suits point-to-point motion. Cartesian space commands the pose of the tool, which suits tasks that need an exact path, a line or an arc; planning is harder and singularities are possible.

**Q: The arm will not move after power-up or a reset. What now?**
A: Check in order whether the arm is in emergency stop or in a fault state, and whether it is enabled. Follow the safe sequence — `reset()`, `clear_faults()`, `enable()` — and move afterwards. If `enable()` is refused, read the faulting axes from `get_state()`; the development manual explains how.

**Q: How do I hand-guide the arm safely?**
A: Enter zero-gravity mode with `zero_g()` and move the arm to the target pose slowly, with both hands. Stay inside the joint soft limits. When you stop, confirm the arm holds its pose. Leave zero-gravity mode when you are done and keep the arm in, or return it to, a safe pose.

**Q: Why does the arm drop after `disable()`?**
A: A disabled joint produces no torque, so the arm falls under gravity. Only disable it while it is supported and nobody is close, or run `home()` first and return to a safe pose.

**Q: The arm will not connect. What should I check?**
A: In order: that the USB cable runs between the control board and the host PC; that `lsusb` lists a device with VID:PID `1d50:606f` (if it does not, check the cable and the power); that your user is in the `dialout` group on Linux; that no other process holds the serial port; and that the firmware is at least `Litearm1.5.0`. If it still will not connect, contact technical support.

**Q: How do I reach technical support?**
A: The NEXFORM ROBOTICS engineering team, or the GitHub organisation at [github.com/nexform-tech](https://github.com/nexform-tech) through Issues.

---

# Related documents and support

This manual covers the appearance of the arm, its specifications and the safety notices. **Mechanical assembly and electrical connection are a separate document**, which you should read alongside this one:

| Document | Contents | Where |
|---|---|---|
| LITEARM-SE installation guide | Unpacking checklist, desktop mounting, column stand, electrical connection and wiring self-check | <https://github.com/nexform-tech/litearm-setup> |
| LITEARM SE software development manual | SDK (Python / C++ / ROS 2), host application, state and errors | <https://github.com/nexform-tech/litearm-python> |

Downloads for the SDK, the LiteArm Studio host application and other related documents: <https://github.com/nexform-tech>

---

> **End of document.** If anything is unclear or you need further information, contact the NEXFORM ROBOTICS engineering team.
