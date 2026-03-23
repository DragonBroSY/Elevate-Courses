---
layout: note
title: "Flightline Reference"
date: 2026-03-18
topics: "Checklists, maneuvers, session debrief notes"
source_hash: bde9225d83fa
---

![Archer-cockpit.jpg](../assets/Archer-cockpit.jpg)
## Emer Desc ##
### ABCDE
A-airspeed 115kts, pwr-idle, bank 3-40deg
B-best area to land
C-checklist
D-declare emer 121.5&7700
E-elt on

# After Start-Flt Inst Check
1. clock ticking with second hand
2. a/s=0
3. att ind 0deg < 5deg, blue over brown
4. alt=field elev within 75'
5. hsi=mag compass within 10deg
6. vsi=0
7. mag compass-no cracks, no bubbles, deviation card present
8. stby att=0deg
9. a/s=0
10. alt within 75' of field elev and within 50' of G500

# Taxi-Flt Inst Check
1. brick outside of turn, turn coord inside
2. hsi/mag compass swing inside of turn
3. att, vsi=0

# Run Up-Flt Inst Check
- set HDG bug to RWY (mag) HDG, Radio1/2: twr/ctaf, ground/atis 

# Pax Brief
- Door: enter top, bottom latch, exit bottom, top latch
- Emer exit: right door, windows x2
- Seat&seatbelts: demonstrate adj seat, put on seatbelt across body and buckle
- fire extingusiher: lcoation, check pointer in green, PASS (point, aim, squeez, sweep)
- No smoking
- PIC authroity: CFI is PIC
- Pos Ex Flight Controls: call, respond, verify, demo

# Pre-Maneuver Check CRAACC
1. clearing turns
2. ref point, pick and turn to it
3. alt *no lower than 1500AGL*
4. a/s
5. config: cruise, landing, clean
	- cruise: TiT PM-throttle 2300, engine inst, tank, pump off, mix lean
	- landing/clean: PT MF-pump on, tank, mix enrich, flap 0/40
6. call

# Before Landing-PLT MF
1. pump
2. landing light
3. tank
4. mix full rich
5. flaps

# Steep Turns
- 100kts
- cruise checklist
- 45deg
- add 100-200 rpm
- a/s use PWR (normal command, ie. not reverse commnad)
- alt use pitch
- ![Pasted image 20260320122248.png](../assets/Pasted%20image%2020260320122248.png)

# Slow Flight
- 1500 rpm, landing config (pump, tank, mix, flaps)
- 50-55kts
- add pwr maintain a/s and alt
- recover: throttle full, flaps 0, Vx, cruise xlist
# Power Off Stall
- 1500 rpm, landing config (pump, tank, mix, flaps)
- capture 66kts, desc 123, pwr-idle, pitch up to 20deg
- recover: AoA, level, pwr, two notch (straight to 10deg), Vx, flaps 0, cruise xlist
# Power On Stall
- 1500 rpm, clean config (pump, tank, mix, flaps)
- 70kts
- full pwr, pitch up to 20deg
- recover: AoA, level, pwr, Vx, cruise xlist

# 03/18
- Airport Ops: Advise twr when runup complete, wait for twr to call while hold short
- Slow flight: holding alt while config to enter maneuver <100' loss
- Pwr-on: climb away after achieve 76kts
- Pwr-off: less nose up after pull power, more realistic sight pic, it will still stall
- Emer Desc: use corr xlist first, it may just fix issue, then ABCDE
# 03/19
- Slow flight: turns no more than 10deg, recovery: can't lose alt, slowww lowering flaps (prevent alt lost), same as go-around flaps need to be retracted slowww "full pwr, slow flaps"
- Emergency: checklist, pitch, bank
- Turn around pt: CRAACC using clean config & best place to land. 1000AGL, 90kts
- Pump always on before proper tank
- Position report: look at HSI tail, don't matter CDI not centered
# 03/20
- PDK turns xwind 400' prior to TPA, as opposed to 300' like everywhere else
- xtk (crosstrack) is 0.6NM to turn from xwind to downwind
- at TPA, pitch, pwr, trim (2000RPM, 90kts, 2000', 1.0 xtk) on downwind, BEFORE LANDING (PLT-MF)
- abeam touchdown point (or traffic) 1500rpm, 10deg flaps, 80kts, lose 200' and 45deg to touchdown point to turn base
- base: 70kts, 25deg flaps, 0.3 xtk (crosstrack) before turning final, G-CASH (glideslope, config (already in), a/s, stablized, heels)
- taxi clearance: 21R via B, E cross 16, advise when runup complete
- traffic pattern scan should be "a/s, alt, xtk"
- Climb with right rudder, turns in traffic pattern should be <20deg

# Airworthiness Check
- ELT 121.5-12 mo, 1 hr use or 50%
- W&B: usable fuel is $48\text{gal}\cdot6=288lbs$ fuel burn is $20gal\cdot6=120lbs$
- Performance: $$ 
\begin{aligned}
ISA=15^\circ C, std lapse rate\rightarrow F.E.@PDK=1000' \rightarrow ISA@PDK=13^\circ C \\
PA=(29.92-baro)\cdot 1000+F.E \\
DA=PA+(OAT-ISA@PDK)\cdot 120 \\
V_A=115 \cdot \sqrt{\frac{Wt_{\text{takeoff or landing}}}{2550}}
\end{aligned}
$$