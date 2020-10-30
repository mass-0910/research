package calculator;

import java.awt.Font;
import java.util.Timer;
import java.util.TimerTask;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;

public class Calc extends JFrame {

	JLabel label = new JLabel();
	JTextField textbox = new JTextField("");
	String nowform = "";
	Font font = new Font("Yu Gothic UI", Font.PLAIN, 32);
	Font font2 = new Font("Yu Gothic UI", Font.PLAIN, 24);
	Font font3 = new Font("Consolas", Font.PLAIN, 24);

	Form form = new Form();

	Timer t = new Timer();
	TimerTask tt = new TimerTask() {
		public void run() {
			if (nowform.equals(textbox.getText())) {
				return;
			}
			form.init(textbox.getText());
			form.split();
			form.splitOut();
			label.setText(form.calc());
			nowform = new String(textbox.getText());
		}
	};

	Calc() {
		setTitle("Calculator");
		setBounds(100, 100, 640, 200);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setResizable(false);
		setVisible(true);
		setLayout(null);
		textbox.setBounds(15, 64, 600, 48);
		textbox.setFont(font2);
		label.setText("Show calcurated answer on here.");
		label.setBounds(10, 10, 500, 28);
		label.setFont(font);
		this.add(textbox);
		this.add(label);

		t.scheduleAtFixedRate(tt, 0, 100);
	}

	public static void main(String[] args) {
		Calc m = new Calc();
	}

}