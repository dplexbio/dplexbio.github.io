---
layout: default
title: Technology
noindex: true
permalink: /technology/
description: Emulsion digital PCR (edPCR) brings the precision of digital PCR to routine, high-throughput testing.
scripts:
  - /assets/js/scrolly.js
---

# Emulsion Digital PCR (edPCR)

Digital PCR counts individual DNA or RNA molecules instead of estimating them. The sample is split into thousands of tiny compartments, PCR runs in each one, and counting the compartments that light up gives an absolute concentration without a standard curve. Until now, that precision has come with expensive instruments, microfluidic chips, and high per-test costs.

DPlexBio's emulsion digital PCR (edPCR) removes those barriers. It is designed as a drop-in replacement for real-time PCR (qPCR) that delivers the performance of digital PCR.

## How it works

<section class="scrolly">
  <ol class="scrolly__steps">
    <li class="scrolly__step">
      <h3>Shake</h3>
      <p>The PCR reaction and our emulsion oil are loaded into a standard-format well plate. A programmable shaker turns each well into an emulsion of droplets in about 10 seconds. No droplet generator or microfluidic chip is needed.</p>
    </li>
    <li class="scrolly__step">
      <h3>Thermocycle</h3>
      <p>The oil sets to stabilize the droplets, and the plate runs on any standard thermocycler, including a real-time PCR instrument you already own.</p>
    </li>
    <li class="scrolly__step" data-panel="1">
      <h3>Image</h3>
      <p>A spinning-disk confocal microscope scans each well in 3D. A reference channel shows every droplet, whether or not it contains a target. Our index-matched oil and aqueous additives make the emulsion optically clear, so the microscope can see more than 2 mm into the well.</p>
    </li>
    <li class="scrolly__step" data-panel="2">
      <h3>Find every droplet</h3>
      <p>Deep-learning software segments the 3D image and identifies each droplet and its size, about 20,000 droplets per well.</p>
    </li>
    <li class="scrolly__step" data-panel="3">
      <h3>Read the PCR signal</h3>
      <p>The software measures the PCR probe fluorescence inside each droplet. Droplets that held a target molecule glow brightly; empty droplets stay dark.</p>
    </li>
    <li class="scrolly__step" data-panel="4">
      <h3>Count and report</h3>
      <p>Each droplet gets a positivity score, and positive and negative droplets separate cleanly into two bands. Counting them, while accounting for droplet size, gives the absolute concentration of the target, with no standard curve needed.</p>
    </li>
  </ol>
  <figure class="scrolly__figure">
    <div class="scrolly__frame">
      <img src="{{ '/assets/images/overview-droplets-to-rain-plot.PNG' | relative_url }}" alt="Four panels showing edPCR analysis of one well: a reference channel image of droplets, the same droplets segmented in color, the PCR probe channel with a few bright positive droplets, and a scatter plot of droplet positivity scores split into positive and negative bands.">
      <span class="scrolly__mask" data-panel="1" style="top: 0; height: 24.3%;"></span>
      <span class="scrolly__mask" data-panel="2" style="top: 24.3%; height: 24.3%;"></span>
      <span class="scrolly__mask" data-panel="3" style="top: 48.6%; height: 23.6%;"></span>
      <span class="scrolly__mask" data-panel="4" style="top: 72.2%; height: 27.8%;"></span>
    </div>
    <figcaption>From droplets to data in a single well.</figcaption>
  </figure>
</section>

## Why droplets of different sizes are a feature

The field has long assumed that accurate digital PCR requires perfectly uniform droplets, which is why conventional systems depend on precision microfluidics. Our team's error analysis, simulations, and experiments showed that accurate digital PCR does not need uniform droplets. A mix of small and large droplets actually **extends the dynamic range**, so one measurement can cover both low and high concentrations.

## Advantages over real-time PCR

- **Absolute quantification.** Results are counted directly, not calibrated against an external standard, which makes assays easier to standardize and reproduce.
- **Tolerance to inhibitors.** Digital PCR is less affected by substances in the sample that interfere with PCR, which simplifies sample preparation.
- **Sensitivity at low copy numbers.** Greater precision when very little target is present, which matters for catching infections early or in people without symptoms.

## Advantages over conventional digital PCR

- **Simple, low-cost workflow.** Droplets are made by shaking, not by expensive instruments or single-use microfluidic chips.
- **Wide dynamic range** from droplets of many sizes.
- **High throughput.** Plates thermocycle on standard instruments in parallel, and imaging speed is set largely by software, so performance can improve through software updates.
- **Multicolor detection.** The optical system supports a reference channel plus nine spectral channels for multiplexed assays.

In testing across thousands of samples, emulsions were stable 99.9% of the time with compatible commercial master mixes. Concentration measurements agree closely with UV absorbance and with competing digital PCR systems.
