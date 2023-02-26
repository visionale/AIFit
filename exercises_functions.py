
def bicep_curl_barbell_side(left_shoulder_angle, left_curl_angle, phase, counter):
    # Bicep Curl with Barbell side view counter logic
    if left_shoulder_angle <= 20:
        if left_curl_angle > 140:
            phase = "excentric"
        if left_curl_angle < 50 and phase == "excentric":
            phase = "concentric"
            counter +=1
            print(counter)

    return counter, phase

def tricep_rope_side(left_shoulder_angle, left_curl_angle, phase, counter):
    # Rope triceps counter logic
    if left_shoulder_angle <= 40:
        if left_curl_angle < 50:
            phase = "excentric"
        if left_curl_angle > 160 and phase == "excentric":
            phase = "concentric"
            counter +=1
            print(counter)

    return counter, phase

def pull_up_back(left_shoulder_angle, right_shoulder_angle, phase, counter):
    # Rope triceps counter logic
    if left_shoulder_angle and right_shoulder_angle > 150:
        phase = "excentric"
    if left_shoulder_angle and right_shoulder_angle <= 50 and phase == "excentric":
        phase = "concentric"
        counter +=1
        print(counter)

    return counter, phase