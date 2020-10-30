class Main {

    Foo f;

    Main(){
        f = new Foo("Hello World");
        f.say10();
    }
    public static void main(String ... args) {
        Main m = new Main();
    }
}

class Foo{

    String str;

    Foo(String str){
        this.str = str;
    }

    public void say10(){
        for (int i = 0; i < 10; i++){
            System.out.println(str);
            str = "aaaaaa";
        }
    }
}