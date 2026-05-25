# FisoThemes' Controller Toolbox for TwinCAT

## Overview

A library of composable building blocks for modelling and building control systems in TwinCAT. It exposes individual signal generators, plant simulators, controller components, filters, signal conditioning, and signal transformation blocks that can be wired together to suit the application. 

For convenience, there is a ready-made production grade `FB_PID` controller or an experimental `FB_LADRC`. You can use these as a template for your own controllers.

## Dependencies

FsControllerToolbox depends on the following libraries:
- **[FsCommon](https://github.com/fisothemes/FisoThemes-Common-Library-for-TwinCAT):** Provides common data structures and utilities.

## Library Structure

| Category         | Description                                                                                 |
|------------------|---------------------------------------------------------------------------------------------|
| **Signals**      | Periodic and aperiodic signal generators (sine, square, triangle, sawtooth, PWM, ramp, ramp profile, white noise, Gaussian noise). |
| **Simulation**   | Discrete-time plant models for closed-loop testing (first-order, second-order, Padé delay). |
| **Control**      | Proportional, integral, derivative, PID, and ADRC controller components.                    |
| **Filters**      | Signal filtering blocks (first-order IIR).                                                  |
| **Conditioning** | Signal shaping blocks (deadband, hysteresis, clamp, rate limiter).                          |
| **Transform**    | Signal transformation blocks (linear scaler, quantizer, gain, bias).                        |

## Usage

### Simulating a Plant

`FB_FirstOrderPlant` and `FB_SecondOrderPlant` simulate linear plants in discrete time. They are useful for testing and tuning controllers before connecting to real hardware.

```js
PROGRAM MAIN
VAR
    fSetpoint : LREAL := 10.0;
    fOutput   : LREAL;
    fbPlant   : FB_FirstOrderPlant(fGain := 1.0, tTau := LTIME#5S);
END_VAR

fbPlant.Input := fSetpoint;
fbPlant.Run();

fOutput := fbPlant.Output;
```

For a second-order plant with overshoot:

```js
VAR
    fSetpoint : LREAL := 5.0;
    fOutput   : LREAL;
    fbPlant   : FB_SecondOrderPlant(fGain := 1.0, fWn := 2.0, fZeta := 0.5);
END_VAR

fbPlant.Input := fSetpoint;
fbPlant.Run();

fOutput := fbPlant.Output;
```

To add transport delay to a plant:

```js
VAR
    fControlOutput : LREAL := 1;
    fPlantOutput   : LREAL;
    fbDelay        : FB_PadeDelay(tDelayTime := LTIME#10S);
    fbPlant        : FB_FirstOrderPlant(fGain := 1.0, tTau := LTIME#5S);
END_VAR

fbDelay.Input := fControlOutput;
fbDelay.Run();

fbPlant.Input := fbDelay.Output;
fbPlant.Run();
fPlantOutput := fbPlant.Output;
```

### Building a PID Controller

The library provides `FB_ProportionalGain`, `FB_Integrator`, `FB_ClampingIntegrator`, `FB_TrackingIntegrator`, and `FB_Differentiator` function blocks that can be composed into any PID form. The error signal (`Setpoint - ProcessVariable`) is computed by the caller.

#### Parallel Form

Each term operates independently on the raw error. `Kp`, `Ki`, and `Kd` are fully decoupled.

<p align="center">
  <img src="./assets/imgs/pid-parallel.drawio.svg" alt="PID Parallel Form" />
</p>

```js
VAR
    fSetpoint : LREAL;
    fOutput   : LREAL;
    fError    : LREAL;
    fbPlant   : FB_FirstOrderPlant(fGain := 1.0, tTau := LTIME#5S);
    fbP       : FB_ProportionalGain(fKp := 2.0);
    fbI       : FB_Integrator(tTn := LTIME#5S);
    fbD       : FB_Differentiator(tTv := LTIME#1S, tTd := LTIME#200MS);
END_VAR

fbI.Maximum := 100.0;
fbI.Minimum := 0.0;

fOutput := fbPlant.Output;

fError := fSetpoint - fOutput;

fbP.Input := fError; fbP.Run();
fbI.Input := fError; fbI.Run();
fbD.Input := fError; fbD.Run();

fbPlant.Input := fbP.Output + fbI.Output + fbD.Output;
fbPlant.Run();
```

#### Standard (Ideal) Form

The integral and derivative terms receive the proportional output rather than the raw error, so `Tn` and `Tv` scale relative to `Kp`. `FB_ClampingIntegrator` prevents integrator windup when the output saturates. The `Mode` property controls the integrator behaviour during saturation: `E_AntiWindupMode.Hold` freezes the integrator output at its last value, while `E_AntiWindupMode.Off` resets it to zero effectively disabling it.

<p align="center">
  <img src="./assets/imgs/pid-ideal-clamping.drawio.svg" alt="PID Ideal Form" />
</p>

```js
VAR
    fSetpoint : LREAL;
    fOutput   : LREAL;
    fError    : LREAL;
    fbPlant   : FB_FirstOrderPlant(fGain := 1.0, tTau := LTIME#5S);
    fbP       : FB_ProportionalGain(fKp := 2.0);
    fbI       : FB_ClampingIntegrator(tTn := LTIME#5S, eMode := E_AntiWindupMode.Hold);
    fbD       : FB_Differentiator(tTv := LTIME#1S, tTd := LTIME#200MS);
    fbClamp   : FB_Clamp(fMaximum := 100.0, fMinimum := 0.0);
END_VAR

fbI.Maximum := fbClamp.Maximum;
fbI.Minimum := fbClamp.Minimum;

fOutput := fbPlant.Output;

fError := fSetpoint - fOutput;

fbP.Input           := fError; fbP.Run();
fbI.Input           := fbP.Output;
fbI.ComparatorInput := fbClamp.Residual; fbI.Run();
fbD.Input           := fbP.Output; fbD.Run();

fbClamp.Input := fbP.Output + fbI.Output + fbD.Output;
fbClamp.Run();

fbPlant.Input := fbClamp.Output;
fbPlant.Run();
```

#### Series (Interacting) Form

The proportional output feeds into the integral term, and the sum of both feeds into the derivative term, coupling all three terms in series. `FB_TrackingIntegrator` is used here for back-calculation anti-windup, feeding the clamp residual back to unwind the integrator gradually when the output saturates.

<p align="center">
  <img src="./assets/imgs/pid-series.drawio.svg" alt="PID Series Form" />
</p>

```js
VAR
    fSetpoint : LREAL;
    fOutput   : LREAL;
    fError    : LREAL;
    fbPlant   : FB_FirstOrderPlant(fGain := 1.0, tTau := LTIME#5S);
    fbP       : FB_ProportionalGain(fKp := 2.0);
    fbI       : FB_TrackingIntegrator(tTn := LTIME#5S, tTt := LTIME#2S200MS);
    fbD       : FB_Differentiator(tTv := LTIME#1S, tTd := LTIME#200MS);
    fbClamp   : FB_Clamp(fMaximum := 100.0, fMinimum := 0.0);
END_VAR

fbI.Maximum := fbClamp.Maximum;
fbI.Minimum := fbClamp.Minimum;

fOutput := fbPlant.Output;

fError := fSetpoint - fOutput;

fbP.Input           := fError; fbP.Run();
fbI.Input           := fbP.Output;
fbI.ComparatorInput := fbClamp.Residual; fbI.Run();
fbD.Input           := fbP.Output + fbI.Output; fbD.Run();

fbClamp.Input := fbP.Output + fbI.Output + fbD.Output;
fbClamp.Run();

fbPlant.Input := fbClamp.Output;
fbPlant.Run();
```

### Using the PID Block

`FB_PID` provides a ready-made ideal-form PID controller with clamped output, clamping-based anti-windup, and bumpless manual-to-auto transfer. The derivative acts on the negated process variable rather than the error, avoiding a derivative spike when the setpoint changes.

<p align="center">
  <img src="./assets/imgs/pid.drawio.svg" alt="PID" />
</p>

```js
VAR
    fSetpoint : LREAL;
    fOutput   : LREAL;
    fbPlant   : FB_FirstOrderPlant(fGain := 2.0, tTau := LTIME#5S);
    fbPID     : FB_PID(
                    fKp      := 2.0,
                    tTn      := LTIME#5S,
                    tTv      := LTIME#1S,
                    tTd      := LTIME#300MS,
                    fMaximum := 100.0,
                    fMinimum := 0.0);
END_VAR

fOutput := fbPlant.Output;

// Optional: Set the integrator bounds.
fbPID.IntegratorBounds.Maximum := fbPID.Maximum;
fbPID.IntegratorBounds.Minimum := fbPID.Minimum;

fbPID.Setpoint := fSetpoint;
fbPID.Feedback := fOutput;
fbPID.Run();

fbPlant.Input := fbPID.Output;
fbPlant.Run();
```

To switch to manual mode and back without a bump:

```js
// Switch to manual and set desired output via Setpoint
fbPID.Mode     := E_ControllerMode.Manual;
fbPID.Setpoint := 50.0; // output will be clamped to [Minimum, Maximum]

// Switch back to auto and observe the output resume smoothly from 50.0
fbPID.Mode := E_ControllerMode.Auto;
```

### Using the ADRC Block

`FB_LADRC` provides a Linear Active Disturbance Rejection Controller (LADRC) which is an alternative to PID. It actively estimates and cancels disturbances, unmodelled dynamics, and plant non-linearities in real time using an Extended State Observer. Unlike PID, it does not require a precise plant model; inaccuracies in `b0` are treated as disturbance and cancelled automatically.

> [!WARNING]
>
> This block is highly experimental. It is not recommended for production use.
>

By default the integral action time is derived automatically as `Tn = 1 / Wc²`. Set `AutoTn := FALSE` to tune `Tn` manually is you experience instability or overshoots.

```js
VAR
    fSetpoint : LREAL;
    fOutput   : LREAL;
    fbPlant   : FB_FirstOrderPlant(fGain := 2.0, tTau := LTIME#5S);
    fbADRC    : FB_LADRC(
	                fB0      := 0.1,
                    fWc      := 5,
                    fWo      := 30,
                    fMaximum := 100.0,
                    fMinimum := 0.0);
END_VAR


fOutput := fbPlant.Output;

// Optional: Tune Tn manually
fbADRC.AutoTn   := FALSE;
fbADRC.Tn	    := LTIME#2S500MS;

fbADRC.Setpoint := fSetpoint;
fbADRC.Feedback := fOutput;
fbADRC.Run();

fbPlant.Input   := fbADRC.Output;
fbPlant.Run();
```


### Generating Signals

Signal generators implement `FsCommon.I_Runnable` and expose a read-only `Output` property.

```js
VAR
    fbSine    : FB_SineWave(tPeriod := LTIME#2S, fAmplitude := 5.0, fBias := 0.0, fPhase := 0.0);
    fbSquare  : FB_SquareWave(tPeriod := LTIME#2S, fAmplitude := 1.0, fBias := 0.0, fPhase := 0.0);
    fbRamp    : FB_Ramp(fStartValue := 0.0, fRate := 1.0);
    fbProfile : FB_RampProfile(fStartValue := 0.0, fTarget := 100.0, tDuration := LTIME#30S);
END_VAR

fbSine.Run();
fbSquare.Run();
fbRamp.Run();
fbProfile.Run();
```

### Generating Signals

Signal generators implement `FsCommon.I_Runnable` and expose a read-only `Output` property. They must be called once per scan (this may change in the future).

```js
VAR
    fbSine    : FB_SineWave(tPeriod := LTIME#2S, fAmplitude := 5.0, fBias := 0.0, fPhase := 0.0);
    fbSquare  : FB_SquareWave(tPeriod := LTIME#2S, fAmplitude := 1.0, fBias := 0.0, fPhase := 0.0);
    fbRamp    : FB_Ramp(fStartValue := 0.0, fRate := 1.0);
    fbProfile : FB_RampProfile(fStartValue := 0.0, fTarget := 100.0, tDuration := LTIME#30S);
END_VAR

fbSine.Run();
fbSquare.Run();
fbRamp.Run();
fbProfile.Run();
```

### Adding Noise to a Simulation

`FB_WhiteNoise` and `FB_GaussianNoise` add realistic measurement noise to simulation signals.

```js
VAR
    fRawSignal   : LREAL;
    fNoisySignal : LREAL;
	fbSquare     : FB_SquareWave(tPeriod := LTIME#2S, fAmplitude := 1.0, fBias := 0.0, fPhase := 0.0);
    fbNoise      : FB_GaussianNoise(fMean := 0.0, fStdDev := 0.1);
END_VAR

fbSquare.Run();
fRawSignal   := fbSquare.Output;
fbNoise.Run();
fNoisySignal := fRawSignal + fbNoise.Output;
```

### Filtering a Signal

`FB_FirstOrderIIRFilter` applies an exponential moving average to smooth a noisy input.

<p align="center">
  <img src="./assets/imgs/filtered-signal.png" alt="Filtered Signal" />
</p>

```js
VAR
    fRawSignal : LREAL;
    fSmoothed  : LREAL;
    fbSignal   : FB_SineWave(tPeriod := LTIME#2S, fAmplitude := 5.0, fBias := 0.0, fPhase := 0.0);
    fbGenRand  : FsCommon.FB_RandomNumberGenerator(0);
    fbFilter   : FB_FirstOrderIIRFilter(fAlpha := 0.1);
END_VAR

fbSignal.Run();

fRawSignal := fbSignal.Output + fbGenRand.NextRangedReal(-0.6, 0.6);

fbFilter.Input := fRawSignal;
fbFilter.Run();

fSmoothed := fbFilter.Output;
```

### Signal Conditioning

`FB_Deadband` suppresses small signals within a configurable band:

```js
VAR
    fbDeadband : FB_Deadband(fMaximum := 0.5, fMinimum := -0.5, eMode := E_DeadbandMode.Zero);
END_VAR

fbDeadband.Input := fError;
fbDeadband.Run();
```

`FB_Hysteresis` implements a two-threshold latch, suited to on/off control such as temperature regulation:

```js
VAR
    fbHysteresis : FB_Hysteresis(fUpperThreshold := 22.0, fLowerThreshold := 18.0);
    bHeaterOn    : BOOL;
END_VAR

fbHysteresis.Input := fTemperature;
fbHysteresis.Run();

bHeaterOn := fbHysteresis.Output;
```

`FB_RateLimiter` constrains how quickly a signal can change:

```js
VAR
    fbLimiter : FB_RateLimiter(fRisingLimit := 10.0, fFallingLimit := 5.0);
END_VAR

fbLimiter.Input := fControlOutput;
fbLimiter.Run();
```

### Signal Transformation

`FB_LinearScaler` maps a signal from one range to another:

```js
VAR
    // Map PID output (0-100%) to valve position (4-20mA)
    fbScaler : FB_LinearScaler(fInputMin := 0.0, fInputMax := 100.0, fOutputMin := 4.0, fOutputMax := 20.0);
END_VAR

fbScaler.Input := fbPID.Output;
fbScaler.Run();
```

## Developer Notes

This is still a work in progress. The API may change as the library grows.