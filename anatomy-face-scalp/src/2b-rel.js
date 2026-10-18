// ---------- extra traced courses ----------
Object.assign(S.greater_occipital_n, { steps: [
  [466, 470, "Arises as the medial branch of the dorsal ramus of C2, emerging below the inferior oblique and curving up around it.", []],
  [473, 410, "Ascends across the suboccipital triangle on semispinalis capitis, then PIERCES semispinalis capitis.", []],
  [471, 355, "PIERCES the trapezius aponeurosis about 2 cm below and lateral to the external occipital protuberance and meets the occipital artery.", ["occipital_a"]],
  [445, 180, "Climbs the back of the scalp in layer C to supply the skin up to the vertex.", ["d_go", "occipitalis"]]] });
Object.assign(S.great_auricular_n, { steps: [
  [410, 560, "Emerges at the nerve point (Erb's point): the midpoint of the posterior border of sternocleidomastoid (C2, C3).", ["scm"]],
  [398, 500, "Ascends obliquely across the superficial surface of SCM, deep to platysma, parallel to and behind the external jugular vein.", ["scm", "platysma", "ejv"]],
  [389, 420, "Divides near the parotid: anterior branch to the skin over the parotid and angle of the mandible, posterior branch to the ear lobule.", ["parotid", "d_c23"]]] });
Object.assign(S.lesser_occipital_n, { steps: [
  [420, 522, "Emerges at the nerve point, hooking around the spinal accessory nerve (C2).", ["scm"]],
  [436, 420, "Ascends along the posterior border of sternocleidomastoid.", ["scm"]],
  [452, 300, "Pierces the deep fascia near the skull to supply the scalp behind and above the ear.", ["d_lo"]]] });
Object.assign(S.buccal_n, { steps: [
  [300, 392, "Arises from the anterior division of V3 and passes between the two heads of lateral pterygoid.", []],
  [262, 400, "Runs forward deep to the ramus, the tendon of temporalis and masseter, onto the outer surface of buccinator.", ["masseter", "temporalis"]],
  [214, 415, "Supplies the skin of the cheek; its branches PIERCE buccinator to supply the buccal mucosa and gum. It does not supply the muscle.", ["buccinator"]]] });
Object.assign(S.parotid_duct, { steps: [
  [335, 360, "Leaves the anterior border of the parotid gland.", ["parotid"]],
  [285, 364, "Crosses superficial to masseter a fingerbreadth below the zygomatic arch, with buccal branches of CN VII and the transverse facial artery.", ["masseter", "cn7_buccal", "transverse_facial_a"]],
  [249, 369, "Turns sharply medially around the anterior border of masseter, through the buccal pad of fat.", ["masseter"]],
  [238, 386, "PIERCES buccinator obliquely and opens on a papilla opposite the upper 2nd molar.", ["buccinator"]]] });
Object.assign(S.cn7_marginal, { steps: [
  [346, 404, "Leaves the lower pole of the parotid gland.", ["parotid"]],
  [318, 492, "Runs forward below the angle of the mandible, deep to platysma; it may dip 1–2 cm below the mandible.", ["platysma", "mandible"]],
  [262, 512, "Crosses SUPERFICIAL to the facial artery and vein at the anterior border of masseter: the danger point in submandibular surgery.", ["facial_a", "facial_v", "masseter"]],
  [170, 476, "Supplies depressor anguli oris, depressor labii inferioris and mentalis.", ["dao", "dli", "mentalis"]]] });
Object.assign(S.cn7_buccal, { steps: [
  [346, 402, "Leaves the anterior border of the parotid with the parotid duct.", ["parotid", "parotid_duct"]],
  [262, 393, "Runs forward across masseter alongside the parotid duct.", ["masseter", "parotid_duct"]],
  [165, 416, "Supplies buccinator, orbicularis oris and the muscles of the upper lip and nose.", ["buccinator", "orb_oris", "zyg_major", "lls"]]] });
Object.assign(S.cn7_zygomatic, { steps: [
  [346, 400, "Leaves the upper anterior border of the parotid gland.", ["parotid"]],
  [255, 332, "Crosses the zygomatic bone toward the lateral angle of the eye.", ["zyg_arch"]],
  [205, 304, "Supplies the lower part of orbicularis oculi: essential for eye closure.", ["orb_oculi"]]] });
Object.assign(S.cn7_cervical, { steps: [
  [346, 406, "Leaves the lower pole of the parotid gland.", ["parotid"]],
  [332, 555, "Descends into the neck, deep to platysma, to supply it.", ["platysma"]]] });
Object.assign(S.mental_n, { steps: [
  [176, 470, "Emerges from the mental foramen below the lower 2nd premolar as the terminal branch of the inferior alveolar nerve.", ["f_mental", "inf_alveolar_n"]],
  [120, 448, "Branches pass up deep to depressor labii inferioris to the skin and mucosa of the lower lip.", ["dli", "orb_oris"]]] });
Object.assign(S.ejv, { steps: [
  [372, 485, "Formed just below the parotid by the posterior division of the retromandibular vein and the posterior auricular vein.", ["rmv", "post_auricular_v"]],
  [388, 590, "Runs down obliquely across the superficial surface of SCM, deep to platysma.", ["scm", "platysma"]],
  [403, 700, "PIERCES the investing layer of deep cervical fascia just above the clavicle and ends in the subclavian vein.", []]] });

// ---------- extra landmark structures (lateral view) ----------
Object.assign(S, {
  styloid: { n: "Styloid process", sys: "bone", grp: "Bone & foramina", w: "Temporal_styloid_process", layer: "deepest",
    lat: ["M384 393 L 392 397 L 352 454 L 347 451 Z"],
    sum: "Slender spike of the temporal bone, just in front of the stylomastoid foramen. Gives origin to stylohyoid, styloglossus and stylopharyngeus.",
    f: { r: "The facial nerve exits between it and the mastoid. Styloglossus, stylopharyngeus and CN IX pass between the external carotid (lateral) and internal carotid (medial).", k: "An elongated, calcified styloid causes Eagle syndrome: throat pain on swallowing or turning the head." } },
  hyoid: { n: "Hyoid bone", sys: "bone", grp: "Bone & foramina", w: "Hyoid_bone",
    lat: ["M204 566 C 230 560, 262 552, 292 546 L 294 553 C 264 560, 232 568, 206 574 Z"],
    sum: "U-shaped bone at C3. The lingual artery loops above its greater horn; digastric and stylohyoid attach to it.",
    f: { p: "Palpable just above the thyroid cartilage, in the angle between the floor of the mouth and the front of the neck." } },
  thyroid_cart: { n: "Thyroid cartilage", sys: "bone", grp: "Bone & foramina", w: "Thyroid_cartilage",
    lat: ["M232 592 L 286 586 L 292 640 L 244 646 Z"],
    sum: "Its upper border (C3/C4) marks the bifurcation of the common carotid artery and the origin of the superior thyroid artery." },
  stylohyoid: { n: "Stylohyoid", sys: "ref", ang: 40, grp: "Landmarks", w: "Stylohyoid_muscle", br: "CN VII",
    lat: ["M384 400 C 350 428, 305 485, 274 544 L 268 541 C 298 482, 344 424, 380 395 Z"],
    sum: "Thin muscle from the styloid process to the hyoid, running along the upper border of the posterior belly of digastric.",
    f: { o: "Posterior surface of the styloid process.", i: "Body of the hyoid; splits around the digastric tendon.", a: "Raises and retracts the hyoid in swallowing.", n: "Facial nerve.", k: "Together with the posterior belly of digastric it is the key landmark of the upper neck: the facial artery, external carotid and hypoglossal nerve all pass deep to these two muscles." } },
  mylohyoid: { n: "Mylohyoid", sys: "ref", ang: 10, grp: "Landmarks", w: "Mylohyoid_muscle", br: "V3", layer: "deepest",
    lat: ["M162 512 L 300 488 L 287 548 L 214 566 L 168 538 Z"],
    sum: "Muscular floor of the mouth. The submandibular gland wraps around its free posterior border.",
    f: { o: "Mylohyoid line of the mandible.", i: "Hyoid and midline raphe.", a: "Raises the floor of the mouth and the hyoid.", n: "Nerve to mylohyoid (V3).", r: "The submental artery runs on its superficial surface." } },
  hyoglossus: { n: "Hyoglossus", sys: "ref", ang: 95, grp: "Landmarks", w: "Hyoglossus", br: "CN XII", layer: "deepest",
    lat: ["M232 556 L 288 547 L 292 500 L 238 494 Z"],
    sum: "Key relation of the floor of the mouth: the lingual artery runs deep to it, while the hypoglossal nerve and lingual nerve lie superficial to it.",
    f: { o: "Greater horn and body of the hyoid.", i: "Side of the tongue.", a: "Depresses the tongue.", n: "Hypoglossal nerve (CN XII)." } },
  sup_constrictor: { n: "Superior constrictor (tonsil bed)", sys: "ref", ang: 0, grp: "Landmarks", w: "Superior_pharyngeal_constrictor_muscle", br: "CN X", layer: "deepest",
    lat: ["M300 418 L 345 412 L 342 482 L 302 488 Z"],
    sum: "Forms the bed of the palatine tonsil. The facial artery loops on its outer surface, separated from the tonsil only by this thin muscle.",
    f: { k: "This is why tonsillectomy can injure the facial artery's tonsillar branch (or the artery itself) and why post-tonsillectomy bleeding can be brisk." } },
  lat_pterygoid: { n: "Lateral pterygoid", sys: "ref", ang: 5, grp: "Landmarks", w: "Lateral_pterygoid_muscle", br: "V3", layer: "deepest",
    lat: ["M262 343 L 352 338 L 356 352 L 344 368 L 266 372 Z"],
    sum: "Muscle of mastication in the infratemporal fossa, deep to the ramus. Key landmark for the maxillary artery and the branches of V3.",
    f: { o: "Upper head: infratemporal surface of the greater wing of sphenoid. Lower head: lateral surface of the lateral pterygoid plate.", i: "Neck of the mandible and the TMJ disc.", a: "Protrudes the mandible and opens the mouth.", n: "Nerve to lateral pterygoid (V3).", r: "The maxillary artery runs superficial (or deep) to its lower head; the buccal nerve passes between its two heads; the lingual and inferior alveolar nerves emerge at its lower border." } },
  med_pterygoid: { n: "Medial pterygoid", sys: "ref", ang: 60, grp: "Landmarks", w: "Medial_pterygoid_muscle", br: "V3", layer: "deepest",
    lat: ["M268 378 L 298 374 L 348 458 L 322 470 Z"],
    sum: "Deep muscle of mastication on the inner side of the ramus, mirroring masseter on the outside.",
    f: { o: "Medial surface of the lateral pterygoid plate.", i: "Inner surface of the ramus and angle.", a: "Closes the jaw.", n: "Nerve to medial pterygoid (V3).", r: "The lingual and inferior alveolar nerves descend on its outer surface, between it and the ramus." } },
  sphenomandibular_lig: { n: "Sphenomandibular ligament", sys: "ref", grp: "Landmarks", w: "Sphenomandibular_ligament", br: "Ligament", line: true, layer: "deepest", wd: 2.4,
    lat: ["~M330 344 C 329 362, 327 384, 324 408"],
    sum: "Ligament from the spine of the sphenoid to the lingula of the mandible. The maxillary artery, maxillary vein and auriculotemporal nerve pass between it and the neck of the mandible." },
  buccal_fat: { n: "Buccal pad of fat", sys: "ref", grp: "Landmarks", w: "Buccal_fat_pad", br: "Fat",
    lat: [oval(252, 384, 13, 17)],
    sum: "Fat pad on buccinator, in front of masseter. The parotid duct runs through it before piercing buccinator." },
  trapezius: { n: "Trapezius", sys: "ref", ang: 75, grp: "Landmarks", w: "Trapezius", br: "CN XI",
    lat: ["M535 368 C 520 430, 486 470, 476 520 C 468 580, 470 640, 478 720 L 436 720 C 440 620, 452 520, 468 448 C 484 410, 506 384, 535 368 Z"],
    sum: "Covers the back of the neck. Its upper attachment (superior nuchal line, external occipital protuberance) is where the occipital artery and greater occipital nerve enter the scalp.",
    f: { o: "Superior nuchal line, external occipital protuberance, ligamentum nuchae, spines of C7–T12.", i: "Lateral clavicle, acromion and spine of scapula.", a: "Elevates and retracts the scapula; extends the head.", n: "Spinal accessory nerve (CN XI).", k: "The greater occipital nerve pierces its aponeurosis about 2 cm lateral and below the external occipital protuberance." } },
  splenius: { n: "Splenius capitis", sys: "ref", ang: 60, grp: "Landmarks", w: "Splenius_capitis_muscle", br: "Dorsal rami", layer: "deepest",
    lat: ["M412 392 L 444 386 L 480 520 L 456 580 Z"],
    sum: "Strap-like muscle deep to SCM and trapezius. The occipital artery runs deep to it after leaving the mastoid groove." },
  semispinalis: { n: "Semispinalis capitis", sys: "ref", ang: 85, grp: "Landmarks", w: "Semispinalis_capitis", br: "Dorsal rami", layer: "deepest",
    lat: ["M456 380 L 502 374 L 488 560 L 466 562 Z"],
    sum: "Large muscle beside the midline at the back of the neck, deep to splenius and trapezius. The greater occipital nerve pierces it." },
  inf_oblique: { n: "Inferior oblique (capitis)", sys: "ref", ang: 50, grp: "Landmarks", w: "Obliquus_capitis_inferior_muscle", br: "C1 dorsal ramus", layer: "deepest",
    lat: ["M430 440 L 444 432 L 478 478 L 467 488 Z"],
    sum: "Suboccipital muscle from the spine of C2 to the transverse process of C1. The greater occipital nerve emerges below it and curves round its lower border." },
  cn12: { n: "Hypoglossal nerve (CN XII)", sys: "nerve", grp: "Cranial nerves in the neck", w: "Hypoglossal_nerve", wd: 2.4,
    lat: ["~M348 425 C 340 470, 332 505, 320 520", "M320 520 C 302 538, 272 540, 246 516"],
    sum: "Motor nerve to the tongue. Descends deep to the posterior belly of digastric, hooks forward round the origin of the occipital artery, crosses the ICA and ECA and runs on hyoglossus.",
    f: { r: "Superficial to the ICA, ECA and loop of the lingual artery; deep to digastric, stylohyoid and the facial vein; on hyoglossus, below the lingual nerve.", k: "Injury: the tongue deviates TO the side of the lesion on protrusion. At risk in carotid endarterectomy." },
    steps: [[348, 425, "Leaves the hypoglossal canal and descends between the ICA and IJV, deep to the posterior belly of digastric.", ["ica", "ijv", "digastric_post"]],
      [320, 520, "Hooks forward round the origin of the occipital artery and crosses superficial to the ICA and ECA.", ["occipital_a", "eca"]],
      [270, 535, "Runs forward on hyoglossus, deep to digastric, stylohyoid and the submandibular gland, to supply the tongue muscles.", ["hyoglossus", "submand_gland"]]] },
  cn11: { n: "Spinal accessory nerve (CN XI)", sys: "nerve", grp: "Cranial nerves in the neck", w: "Accessory_nerve", wd: 2.2,
    lat: ["~M346 426 C 365 450, 385 470, 400 486", "M400 486 C 415 510, 428 530, 435 546 C 448 580, 460 612, 468 642"],
    sum: "Motor to sternocleidomastoid and trapezius. Crosses the posterior triangle superficially, where it is easily injured.",
    f: { k: "Lesion in the posterior triangle (e.g. lymph node biopsy): weak shrug and shoulder droop, with SCM spared because its branch leaves first." },
    steps: [[346, 426, "Leaves the jugular foramen and crosses the IJV, passing deep to the posterior belly of digastric and the occipital artery.", ["ijv", "digastric_post", "occipital_a"]],
      [400, 486, "Enters and supplies the deep surface of sternocleidomastoid.", ["scm"]],
      [435, 546, "Emerges from the posterior border of SCM just above the nerve point (the lesser occipital nerve hooks round it here) and crosses the posterior triangle.", ["scm", "lesser_occipital_n"]],
      [468, 640, "Passes under the anterior border of trapezius to supply it.", ["trapezius"]]] }
});

// ---------- relations at each step: d = deep to, s = superficial to, p = pierces / passes through, w = runs with ----------
// A word that is a structure id becomes a link and lights up on the model; anything in brackets is a note.
const REL = {
  facial_a: [
    { d: ["platysma", "investing fascia"], w: ["lingual_a (may share a linguofacial trunk)"] },
    { d: ["digastric_post", "stylohyoid"], s: ["sup_constrictor", "styloid (styloglossus)"] },
    { d: ["submand_gland (grooves it, then arches over its upper border)"], s: ["mylohyoid (submental branch runs on it)"], w: ["submental_a"] },
    { d: ["platysma", "skin"], s: ["mandible"], w: ["facial_v (just behind)", "cn7_marginal (crosses superficially)"] },
    { d: ["platysma", "risorius", "zyg_major", "zyg_minor"], s: ["buccinator", "lao"] },
    { d: ["zyg_major", "risorius"], s: ["buccinator"], w: ["sup_labial_a", "inf_labial_a (run deep to orb_oris)"] },
    { d: ["llsan"], w: ["lat_nasal_a"] },
    { p: ["llsan (runs in its fibres)"], w: ["angular_v (lateral)", "dorsal_nasal_a (anastomosis)"] }],
  facial_v: [
    { w: ["supratrochlear_v", "supraorbital_v"] },
    { d: ["zyg_major", "zyg_minor"], w: ["facial_a (in front)"] },
    { w: ["deep_facial_v"] },
    { d: ["risorius", "platysma"], s: ["buccinator", "masseter"] },
    { d: ["platysma", "cn7_marginal"], s: ["mandible"], w: ["facial_a (in front)"] },
    { s: ["submand_gland"], w: ["rmv (anterior division)"] }],
  angular_v: [{ w: ["angular_a (medial)"] }, { w: ["sup_ophthalmic_v"] }, {}],
  sta: [
    { w: ["parotid (inside it)", "stv"] },
    { w: ["transverse_facial_a"] },
    { d: ["skin", "auricularis (anterior)"], s: ["zyg_arch (posterior root)"], w: ["stv", "auriculotemporal_n (behind)", "cn7_temporal (in front)"] },
    { d: ["skin (layer C)"], s: ["temporal fascia", "temporalis"], w: ["stv"] },
    { w: ["supraorbital_a", "supratrochlear_a (anastomoses)"] },
    { w: ["occipital_a", "post_auricular_a (anastomoses)"] }],
  occipital_a: [
    { w: ["cn12 (hooks round its origin)"] },
    { d: ["digastric_post"], s: ["ica", "ijv", "cn11", "CN X"] },
    { d: ["scm", "splenius", "longissimus capitis"], s: ["mastoid (occipital groove, medial to it)"] },
    { p: ["deep fascia between the scm and trapezius attachments"], s: ["semispinalis"], w: ["greater_occipital_n (medial)"] },
    { s: ["galea", "occipitalis"], w: ["greater_occipital_n"] }],
  post_auricular_a: [{ w: ["parotid"] }, { w: ["mastoid (between it and the ear cartilage)"] }, { s: ["auricularis (posterior)"] }],
  eca: [
    { d: ["scm (anterior border)", "platysma"], w: ["ica (posterolateral at first)"] },
    {}, {},
    { d: ["digastric_post", "stylohyoid", "cn12"], s: ["styloid (styloglossus, stylopharyngeus and CN IX separate it from the ICA)"] },
    { d: ["cn7", "rmv"], p: ["parotid (enters it)"] },
    { d: ["parotid", "cn7", "rmv"] }],
  maxillary_a: [
    { d: ["mandible (medial to its neck)"], s: ["sphenomandibular_lig (passes between it and the mandible)"] },
    { w: ["inf_alveolar_n", "auriculotemporal_n"] },
    { w: ["lat_pterygoid (superficial or deep to its lower head)"], s: ["med_pterygoid"] },
    { p: ["pterygomaxillary fissure"] }],
  supraorbital_a: [{ p: ["supraorbital notch"], w: ["supraorbital_n"] }, { d: ["frontalis"], p: ["frontalis"] }, { s: ["galea"], w: ["sta (anastomosis)"] }],
  supraorbital_n: [{ p: ["supraorbital notch"], w: ["supraorbital_a"] }, { d: ["frontalis"], p: ["frontalis"] }, { s: ["galea"] }],
  infraorbital_n: [
    { p: ["inferior orbital fissure"] },
    { d: ["inferior rectus", "orbital fat (in the orbital floor)"], w: ["infraorbital_a"] },
    { d: ["lls"], s: ["lao"], p: ["infraorbital foramen"] },
    { d: ["orb_oculi", "lls", "zyg_minor"] }],
  auriculotemporal_n: [
    { d: ["lat_pterygoid"], w: ["middle_meningeal_a (its two roots encircle it)"] },
    { d: ["parotid (upper part)"], w: ["mandible (between its neck and the sphenomandibular ligament)", "sphenomandibular_lig"] },
    { s: ["zyg_arch"], w: ["sta (in front)", "stv"] },
    { s: ["temporal fascia"] }],
  cn7: [
    { p: ["f_stylomastoid"], w: ["styloid (in front)", "mastoid (behind)", "stylomastoid artery"] },
    { w: ["post_auricular_n", "digastric_post", "stylohyoid (supplies both)"] },
    { s: ["rmv", "eca"], p: ["parotid (enters its posteromedial surface)"] },
    { w: ["parotid (divides inside it)"] }],
  cn7_temporal: [{ w: ["parotid"] }, { d: ["skin", "superficial temporal fascia"], s: ["zyg_arch"] }, { s: ["frontalis (enters its deep surface)"] }],
  rmv: [{ w: ["parotid (inside it)"] }, { d: ["cn7"], s: ["eca"] }, {}, { w: ["facial_v"] }, { w: ["post_auricular_v"] }],
  stv: [{ w: ["sta"] }, {}, { s: ["zyg_arch"], w: ["sta (in front)", "auriculotemporal_n (behind)"] }, { p: ["parotid (enters it)"], w: ["maxillary_v"] }],
  greater_occipital_n: [
    { w: ["inf_oblique (curves round its lower border)"] },
    { p: ["semispinalis"], d: ["splenius", "trapezius"] },
    { p: ["trapezius (aponeurosis)"], w: ["occipital_a (lateral)"] },
    { s: ["galea", "occipitalis"], w: ["occipital_a"] }],
  great_auricular_n: [{ w: ["scm (posterior border, nerve point)"] }, { d: ["platysma"], s: ["scm"], w: ["ejv (in front)"] }, { w: ["parotid"] }],
  lesser_occipital_n: [{ w: ["cn11 (hooks round it)"] }, { w: ["scm (posterior border)"] }, { p: ["deep fascia"] }],
  buccal_n: [{ p: ["lat_pterygoid (between its two heads)"] }, { d: ["masseter", "temporalis (tendon)"] }, { s: ["buccinator"], p: ["buccinator (branches to the mucosa)"] }],
  parotid_duct: [{ w: ["parotid"] }, { s: ["masseter"], w: ["cn7_buccal", "transverse_facial_a (above)"] }, { p: ["buccal_fat"] }, { p: ["buccinator"] }],
  cn7_marginal: [{ w: ["parotid"] }, { d: ["platysma"] }, { d: ["platysma"], s: ["facial_a", "facial_v"] }, { s: ["dao", "dli (enters their deep surfaces)"] }],
  cn7_buccal: [{ w: ["parotid_duct"] }, { s: ["masseter"], w: ["parotid_duct"] }, { s: ["buccinator"] }],
  cn7_zygomatic: [{ w: ["parotid"] }, { s: ["zyg_arch"] }, { s: ["orb_oculi (enters its deep surface)"] }],
  cn7_cervical: [{ w: ["parotid"] }, { d: ["platysma"] }],
  mental_n: [{ p: ["f_mental"], w: ["mental_a"] }, { d: ["dli"] }],
  ejv: [{ w: ["rmv", "post_auricular_v"] }, { d: ["platysma"], s: ["scm"], w: ["great_auricular_n (behind)"] }, { p: ["investing layer of deep cervical fascia"] }]
};
const REL_LABEL = { d: "Deep to", s: "Superficial to", p: "Pierces / passes through", w: "Runs with" };
function relParts(str) {
  const m = String(str).match(/^([a-z0-9_]+)(.*)$/);
  if (m && S[m[1]]) return { id: m[1], text: S[m[1]].n.replace(/ \((V1|V2|V3|C2|C3|C2, C3|mastication|CN VII)\)$/, "") + m[2] };
  return { id: null, text: String(str) };
}
function relIds(id, i) {
  const r = (REL[id] || [])[i]; if (!r) return [];
  return ["d", "s", "p", "w"].flatMap(k => (r[k] || []).map(x => relParts(x).id).filter(Boolean));
}
REL.cn12 = [{ d: ["digastric_post"], w: ["ica", "ijv"] }, { s: ["ica", "eca"], w: ["occipital_a (hooks round its origin)"] }, { d: ["digastric_post", "stylohyoid", "submand_gland"], s: ["hyoglossus"] }];
REL.cn11 = [{ d: ["digastric_post", "occipital_a"], s: ["ijv"] }, { p: ["scm"] }, { d: ["skin and investing fascia (very superficial: easily injured)"] }, { d: ["trapezius"] }];
