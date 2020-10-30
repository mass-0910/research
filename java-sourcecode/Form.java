package calculator;

import java.util.ArrayList;

public class Form {

	String form;
	int pos;
	ArrayList<String> splittedForm = new ArrayList<String>();
	ArrayList<Double> entity = new ArrayList<Double>();
	double entitynum = 0;

	Form() {
		pos = 0;
	}

	public void init(String form) {
		this.form = form;
		pos = 0;
		splittedForm.clear();
		entity.clear();
		entitynum = 0.0;
	}

	public void split() {
		String bag = "";
		String operator = "\\+|-|\\*|/|\\(|\\)|%|sin|cos|tan|abs|log|sqrt|cbrt|pow|exp|asin|acos|atan|deg|rad|PI|E|\\{|\\}";
		while (pos < form.length()) {
			space();
			bag = pack(bag);
			if (bag.matches("^[0-9]+$")) {
				for (;;) {
					if (pos == form.length()) {
						splittedForm.add("number");
						entity.add(Double.valueOf(bag));
						break;
					}
					bag = pack(bag);
					if (!bag.matches("^[0-9]+[.]?[0-9]*$")) {
						bag = bag.substring(0, bag.length() - 1);
						pos--;
						splittedForm.add("number");
						entity.add(Double.valueOf(bag));
						bag = "";
						break;
					}
				}
			}
			if (bag.matches(operator)) {
				splittedForm.add(bag);
				entity.add(Double.valueOf(0));
				bag = "";
			}
		}
		splittedForm.add("end");
		entity.add(Double.valueOf(0));
		splittedForm.add("end");
		entity.add(Double.valueOf(0));
		splittedForm.add("end");
		entity.add(Double.valueOf(0));
		splittedForm.add("end");
		entity.add(Double.valueOf(0));
		splittedForm.add("end");
		entity.add(Double.valueOf(0));
		splittedForm.add("end");
		entity.add(Double.valueOf(0));
	}
	
	private void space() {
		while (form.charAt(pos) == ' ') {
			if (pos == form.length() - 1) {
				break;
			} else {
				pos++;
			}
		}
	}

	private String pack(String bag) {
		bag += String.valueOf(form.charAt(pos));
		pos++;
		return bag;
	}

	public String calc() {
		pos = 0;
		return String.valueOf(expr());
	}

	private double expr() {
		System.out.println("expr");
		double x = term();
		for (;;) {
			switch (peek()) {
			case "+":
				System.out.println("" + (pos - 1) + " -> " + pos);
				x += term();
				continue;
			case "-":
				System.out.println("" + (pos - 1) + " -> " + pos);
				x -= term();
				continue;
			default:
				System.out.println("" + (pos - 1) + " -> " + pos);
			}
			pos--;
			break;
		}
		System.out.println("expr : " + x);
		return x;
	}

	private double term() {
		System.out.println(" term");
		Double x;
		switch (peek()) {
		case "-":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = -number();
			break;
		case "+":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = number();
			break;
		case "sin":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.sin(number());
			break;
		case "cos":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.cos(number());
			break;
		case "tan":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.tan(number());
			break;
		case "asin":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.asin(number());
			break;
		case "acos":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.acos(number());
			break;
		case "atan":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.atan(number());
			break;
		case "abs":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.abs(number());
			break;
		case "deg":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.toDegrees(number());
			break;
		case "rad":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.toRadians(number());
			break;
		case "log":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			if (peek().equals("{")) {
				Double base = expr();
				peek();
				x = Math.log(number()) / Math.log(base);
			} else {
				pos--;
				x = Math.log(number());
			}
			break;
		case "sqrt":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.sqrt(number());
			break;
		case "cbrt":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.cbrt(number());
			break;
		case "exp":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x = Math.exp(number());
			break;
		case "pow":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			if (peek().equals("{")) {
				Double pownum = expr();
				peek();
				x = Math.pow(number(), pownum);
			} else {
				pos--;
				x = Math.pow(number(), 2);
			}
			break;
		default:
			System.out.println(" " + (pos - 1) + " -> " + pos);
			pos--;
			System.out.println(" " + (pos + 1) + " -> " + pos);
			x = number();
			break;
		}
		switch (peek()) {
		case "*":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x *= term();
			break;
		case "/":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x /= term();
			break;
		case "%":
			System.out.println(" " + (pos - 1) + " -> " + pos);
			x %= term();
			break;
		default:
			System.out.println(" " + (pos - 1) + " -> " + pos);
			pos--;
			System.out.println(" " + (pos + 1) + " -> " + pos);
			break;
		}
		System.out.println(" term : " + x);
		return x;
	}

	private double number() {
		System.out.println("  number");
		Double x;
		switch (peek()) {
		case "(":
			System.out.println("  " + (pos - 1) + " -> " + pos);
			x = expr();
			peek();
			break;
		case "number":
			System.out.println("  " + (pos - 1) + " -> " + pos);
			x = entitynum;
			break;
		case "PI":
			System.out.println("  " + (pos - 1) + " -> " + pos);
			x = Math.PI;
			break;
		case "E":
			System.out.println("  " + (pos - 1) + " -> " + pos);
			x = Math.E;
			break;
		default:
			System.out.println("  " + (pos - 1) + " -> " + pos);
			x = 0.0;
		}
		System.out.println("  number : " + x);
		return x;
	}

	private String peek() {
		String ret = splittedForm.get(pos);
		if (ret.equals("number")) {
			entitynum = entity.get(pos).doubleValue();
		}
		pos++;
		return ret;
	}

	public void splitOut() {
		for (int i = 0; i < splittedForm.size(); i++) {
			System.out.print(splittedForm.get(i) + ",");
		}
		System.out.println();
		for (int i = 0; i < splittedForm.size(); i++) {
			System.out.print(entity.get(i) + ",");
		}
		System.out.println();
	}

}