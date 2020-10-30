#include <stdio.h>
#include <string.h>
#include <jvmti.h>

static jvmtiEnv *jvmti = 0;
    
static void JNICALL ClassPrepare(jvmtiEnv *jvmti_env, JNIEnv *jni_env, jthread thread, jclass klass);
static void JNICALL SingleStep(jvmtiEnv *jvmti_env, JNIEnv* jni_env, jthread thread, jmethodID method, jlocation location);
static jstring getClassName(JNIEnv *env, jclass klass);
    
JNIEXPORT jint JNICALL Agent_OnLoad(JavaVM *vm, char *options, void *reserved) {
    (*vm)->GetEnv(vm, (void**)&jvmti, JVMTI_VERSION);
    
    jvmtiEventCallbacks callbackTable = { 0 };
    callbackTable.ClassPrepare = ClassPrepare;
    callbackTable.SingleStep = SingleStep;

    jvmtiCapabilities tmp = {0};

    // (*jvmti)->GetCapabilities(jvmti, &tmp);
    // if(tmp.can_generate_single_step_events){
    //     puts("can detect single step");
    // }else{
    //     puts("cannot detect single step");
    // }

    // tmp.can_generate_single_step_events = 1;
    // (*jvmti)->AddCapabilities(jvmti, &tmp);

    // tmp.can_generate_single_step_events = 0;

    // (*jvmti)->GetCapabilities(jvmti, &tmp);
    // if(tmp.can_generate_single_step_events){
    //     puts("can detect single step");
    // }else{
    //     puts("cannot detect single step");
    // }
    
    
    (*jvmti)->SetEventCallbacks(jvmti, &callbackTable, sizeof(callbackTable));
    
    (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_ENABLE, JVMTI_EVENT_CLASS_PREPARE, NULL);
    
    (*jvmti)->SetEventNotificationMode(jvmti, JVMTI_ENABLE, JVMTI_EVENT_SINGLE_STEP, NULL);

    (*jvmti)->GetPotentialCapabilities(jvmti, &tmp);
    if(tmp.can_generate_single_step_events){
        puts("can detect single step");
    }else{
        puts("cannot detect single step");
    }

    printf("agent is loading...\n");
    return 0;
}
    
JNIEXPORT void JNICALL Agent_OnUnload(JavaVM *vm) {
    (*jvmti)->DisposeEnvironment(jvmti);
    printf("agent is unloading...\n");
}
    
static void JNICALL ClassPrepare(jvmtiEnv *jvmti_env, JNIEnv *jni_env, jthread thread, jclass klass) {
    jstring strObj = getClassName(jni_env, klass);
    const char *str = (*jni_env)->GetStringUTFChars(jni_env, strObj, NULL);
    
    if(strcmp(str, "Main") == 0 || strcmp(str, "Foo") == 0){
        printf("%s prepared.\n", str);
    }
    
    (*jni_env)->ReleaseStringUTFChars(jni_env, strObj, str);
}

static void JNICALL SingleStep(jvmtiEnv *jvmti_env, JNIEnv* jni_env, jthread thread, jmethodID method, jlocation location){
    puts("single step");
}
    
static jstring getClassName(JNIEnv *env, jclass klass) {
    jclass cls = (*env)->GetObjectClass(env, klass);
    jmethodID mid =
            (*env)->GetMethodID(env, cls, "getName", "()Ljava/lang/String;"); 
    jstring strObj = (jstring)(*env)->CallObjectMethod(env, klass, mid);
    
    return strObj;
}